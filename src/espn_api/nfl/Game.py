from datetime import datetime
from espn_api.utilities.request import get as get_request
from espn_api.nfl.NFLData import NFLData
from espn_api.nfl.Odds import Odds


class Game(NFLData):
    def __init__(self, game_data, odds_data=None):
        """
        Initialize a Game object with game data and optional odds data
        """
        self.game_id = game_data.get('id')
        self.status = game_data.get('status', {}).get('type', {}).get('name')
        self.date = self._parse_datetime(game_data.get('date'))
        self.venue = game_data.get('competitions', [{}])[0].get('venue', {}).get('fullName')
        self.location = game_data.get('competitions', [{}])[0].get('location')
        self.attendance = game_data.get('competitions', [{}])[0].get('attendance')
        
        # Team information
        self.competitors = self._parse_competitors(game_data.get('competitions', [{}])[0].get('competitors', []))
        self.home_team = next((team for team in self.competitors if team.get('homeAway') == 'home'), {})
        self.away_team = next((team for team in self.competitors if team.get('homeAway') == 'away'), {})
        
        # Odds
        self.odds = Odds(odds_data) if odds_data else None
        
        # Game details
        self.details = {
            'season': game_data.get('season', {}).get('year'),
            'week': game_data.get('week', {}).get('number'),
            'season_type': game_data.get('season', {}).get('type'),
            'neutral_site': game_data.get('competitions', [{}])[0].get('neutralSite', False),
            'conference_competition': game_data.get('competitions', [{}])[0].get('conferenceCompetition', False),
            'play_by_play_available': game_data.get('playByPlaySource'),
            'broadcasts': [broadcast.get('names', []) for broadcast in game_data.get('competitions', [{}])[0].get('broadcasts', [])]
        }

    def _parse_competitors(self, competitors_data):
        """Parse the competitors data into a more usable format"""
        parsed = []
        for competitor in competitors_data:
            team = competitor.get('team', {})
            parsed.append({
                'id': team.get('id'),
                'name': team.get('displayName'),
                'abbreviation': team.get('abbreviation'),
                'score': competitor.get('score'),
                'homeAway': competitor.get('homeAway'),
                'winner': competitor.get('winner'),
                'record': {
                    'wins': competitor.get('record', [{}])[0].get('items', [{}])[0].get('stats', [{}])[0].get('value'),
                    'losses': competitor.get('record', [{}])[0].get('items', [{}])[1].get('stats', [{}])[0].get('value'),
                    'ties': competitor.get('record', [{}])[0].get('items', [{}])[2].get('stats', [{}])[0].get('value')
                },
                'logo': team.get('logo')
            })
        return parsed
    
    def _parse_datetime(self, date_str):
        """Parse the datetime string from ESPN format"""
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, '%Y-%m-%dT%H:%MZ')
        except:
            return date_str

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