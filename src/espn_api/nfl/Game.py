from datetime import datetime
from espn_api.utilities.request import get as get_request
from espn_api.nfl.NFLData import NFLData
from espn_api.nfl.Odds import Odds


class Game(NFLData):
    def __init__(self, game_data, odds_data=None):
        """
        Initialize a Game object with game data and optional odds data
        
        Args:
            game_data: Raw game data from ESPN API
            odds_data: Raw odds data from ESPN API (optional)
        """
        self.raw_data = game_data
        competitions = game_data.get('competitions', [{}])
        self.competition = competitions[0] if competitions else {}
        
        # Basic game info
        self.game_id = game_data.get('id')
        self.name = game_data.get('name', '')
        self.short_name = game_data.get('shortName', '')
        self.date = self._parse_datetime(game_data.get('date'))
        
        # Status information
        self.status = self._get_nested_value(game_data, ['status', 'type', 'name'])
        
        # Venue information
        venue = self.competition.get('venue', {})
        self.venue = {
            'id': venue.get('id'),
            'name': venue.get('fullName'),
            'address': venue.get('address', {}),
            'indoor': venue.get('indoor'),
            'grass': venue.get('grass')
        }

        self.attendance = self.competition.get('attendance')
        
        teams_short = self.short_name.split('@')
        # Team information
        self.home_team = {
            'id': self._get_nested_value(self.competition, ['competitors', 0, 'id']),
            'name': teams_short[1].strip(),
        }

        self.away_team = {
            'id': self._get_nested_value(self.competition, ['competitors', 1, 'id']),
            'name': teams_short[0].strip(),
        }
        
        # Odds
        self.odds = Odds(odds_data) if odds_data else None
        
        # Game details
        self.details = {
            'season': self._get_nested_value(game_data, ['season', 'year']),
            'week': self._get_nested_value(game_data, ['week', 'number']),
            'season_type': self._get_nested_value(game_data, ['season', 'type']),
            'neutral_site': self.competition.get('neutralSite', False),
            'conference_competition': self.competition.get('conferenceCompetition', False),
            'play_by_play_available': self._get_nested_value(game_data, ['playByPlaySource', 'state']) == 'full',
            'broadcasts': self._get_broadcast_info(),
            'format': self.competition.get('format', {})
        }
        
    
    def _parse_datetime(self, date_str):
        """
        Parse the datetime string from ESPN format
        
        Args:
            date_str: Date string in format 'YYYY-MM-DDTHH:MMZ'
            
        Returns:
            datetime object if parsing succeeds, original string if it fails, or None if input is None
        """
        if not date_str:
            return None
            
        try:
            # Handle both '2025-01-04T21:30Z' and '2025-01-04T21:30:00Z' formats
            if date_str.count(':') == 1:  # No seconds
                return datetime.strptime(date_str, '%Y-%m-%dT%H:%MZ')
            return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        except (ValueError, TypeError) as e:
            return date_str
            
    def _get_nested_value(self, data, keys, default=None):
        """
        Safely get a value from a nested dictionary using a list of keys
        
        Args:
            data: The dictionary to search
            keys: List of keys/indices to traverse
            default: Default value to return if any key is not found
            
        Returns:
            The value if found, otherwise default
        """
        try:
            for key in keys:
                if isinstance(data, (list, tuple)) and isinstance(key, int):
                    data = data[key] if abs(key) < len(data) else default
                elif isinstance(data, dict):
                    data = data.get(key, default)
                else:
                    return default
                if data is None:
                    return default
            return data
        except (KeyError, IndexError, TypeError, AttributeError):
            return default
            
    def _get_broadcast_info(self):
        """Extract broadcast information from the competition data"""
        broadcasts = []
        for broadcast in self.competition.get('broadcasts', []):
            if 'names' in broadcast and isinstance(broadcast['names'], list):
                broadcasts.extend(name for name in broadcast['names'] if name)
        return broadcasts

    @classmethod
    async def _get_async(cls, game_id):
        """
        Get game data by game ID
        
        Args:
            game_id (int): The ESPN game ID
            
        Returns:
            Game: A Game object with the game data
        """
        if not isinstance(game_id, int):
            raise TypeError("game_id must be an integer")
            
        try:
            # Define all the API endpoints we want to query
            base_url = f"http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{game_id}"
            urls = [
                base_url,  # Main game data
                f"{base_url}/competitions/{game_id}/odds",  # Odds data
                f"{base_url}/competitions/{game_id}/boxscore",  # Boxscore data
                f"{base_url}/competitions/{game_id}/roster"  # Roster data
            ]
            
            # Make all requests in parallel
            all_data = await get_request(urls)
            game_data = all_data[0]
            odds_data = all_data[1]
            # TODO: add others here later
            
            # Create and return Game object with all the data
            return cls(game_data, odds_data)
            
        except Exception as e:
            raise Exception(f"Error fetching game data: {str(e)}")
    
    def __str__(self):
        return f"{self.away_team.get('name')} @ {self.home_team.get('name')} - {self.date.strftime('%Y-%m-%d %H:%M') if isinstance(self.date, datetime) else self.date}"