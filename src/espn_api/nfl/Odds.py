from espn_api.utilities.request import get as get_request
from espn_api.nfl.NFLData import NFLData

class Odds(NFLData):
    def __init__(self, odds_data):
        """
        Initialize an Odds object with odds data
        
        Args:
            odds_data (dict): Raw odds data from ESPN API
        """
        self.raw_data = odds_data
        self.provider = self._get_provider(odds_data)
        self.details = self._parse_odds_details(odds_data)
        self.spread = self._parse_spread(odds_data)
        self.moneyline = self._parse_moneyline(odds_data)
        self.over_under = self._parse_over_under(odds_data)
        self.last_updated = self._parse_last_updated(odds_data)
    
    def _get_provider(self, odds_data):
        """Extract the odds provider information"""
        if not odds_data or not isinstance(odds_data, dict):
            return None
            
        provider = odds_data.get('provider', {})
        return {
            'id': provider.get('id'),
            'name': provider.get('name'),
            'priority': provider.get('priority')
        }
    
    def _parse_odds_details(self, odds_data):
        """Parse the main odds details"""
        if not odds_data or not isinstance(odds_data, dict):
            return {}
            
        return {
            'details': odds_data.get('details'),
            'over_under': odds_data.get('overUnder'),
            'over_odds': odds_data.get('overOdds'),
            'under_odds': odds_data.get('underOdds'),
            'spread_odds': odds_data.get('spreadOdds'),
            'away_team_odds': odds_data.get('awayTeamOdds', {}).get('favorite'),
            'home_team_odds': odds_data.get('homeTeamOdds', {}).get('favorite'),
            'money_line_away': odds_data.get('moneyLineAway'),
            'money_line_home': odds_data.get('moneyLineHome'),
            'money_line_draw': odds_data.get('moneyLineDraw'),
            'open_date': odds_data.get('openDate'),
            'last_updated': odds_data.get('lastUpdated'),
            'point_spread_away': odds_data.get('pointSpreadAway'),
            'point_spread_home': odds_data.get('pointSpreadHome'),
            'point_spread_away_line': odds_data.get('pointSpreadAwayLine'),
            'point_spread_home_line': odds_data.get('pointSpreadHomeLine'),
            'score_away': odds_data.get('scoreAway'),
            'score_home': odds_data.get('scoreHome'),
            'vig_away': odds_data.get('vigAway'),
            'vig_home': odds_data.get('vigHome')
        }
    
    def _parse_spread(self, odds_data):
        """Parse spread data"""
        if not odds_data or not isinstance(odds_data, dict):
            return {}
            
        return {
            'away': {
                'point_spread': odds_data.get('pointSpreadAway'),
                'point_spread_line': odds_data.get('pointSpreadAwayLine'),
                'vig': odds_data.get('vigAway'),
                'odds': odds_data.get('spreadOdds')
            },
            'home': {
                'point_spread': odds_data.get('pointSpreadHome'),
                'point_spread_line': odds_data.get('pointSpreadHomeLine'),
                'vig': odds_data.get('vigHome'),
                'odds': -odds_data.get('spreadOdds') if odds_data.get('spreadOdds') else None
            }
        }
    
    def _parse_moneyline(self, odds_data):
        """Parse moneyline data"""
        if not odds_data or not isinstance(odds_data, dict):
            return {}
            
        return {
            'away': {
                'odds': odds_data.get('moneyLineAway'),
                'favorite': odds_data.get('awayTeamOdds', {}).get('favorite')
            },
            'home': {
                'odds': odds_data.get('moneyLineHome'),
                'favorite': odds_data.get('homeTeamOdds', {}).get('favorite')
            },
            'draw': {
                'odds': odds_data.get('moneyLineDraw')
            }
        }
    
    def _parse_over_under(self, odds_data):
        """Parse over/under data"""
        if not odds_data or not isinstance(odds_data, dict):
            return {}
            
        return {
            'line': odds_data.get('overUnder'),
            'over_odds': odds_data.get('overOdds'),
            'under_odds': odds_data.get('underOdds')
        }
    
    def _parse_last_updated(self, odds_data):
        """Parse last updated timestamp"""
        if not odds_data or not isinstance(odds_data, dict):
            return None
        return odds_data.get('lastUpdated')
    
    @classmethod
    async def _get_async(cls, game_id):
        """
        Get odds data by game ID
        
        Args:
            game_id (int): The ESPN game ID
            
        Returns:
            Odds: An Odds object with the odds data
        """
        if not isinstance(game_id, int):
            raise TypeError("game_id must be an integer")
            
        try:
            # Get odds data
            odds_url = f"http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{game_id}/competitions/{game_id}/odds"
            odds_data = await get_request(odds_url)
            
            # Create and return Odds object
            return cls(odds_data)
            
        except Exception as e:
            raise Exception(f"Error fetching odds data: {str(e)}")
    
    def get_favorite(self):
        """Get the favorite team based on the odds"""
        if self.moneyline['home']['favorite']:
            return 'home'
        elif self.moneyline['away']['favorite']:
            return 'away'
        return None
    
    def get_underdog(self):
        """Get the underdog team based on the odds"""
        if self.moneyline['home']['favorite'] is False:
            return 'home'
        elif self.moneyline['away']['favorite'] is False:
            return 'away'
        return None
    
    def get_implied_probability(self, odds):
        """
        Convert American odds to implied probability
        
        Args:
            odds (int): American odds (positive or negative)
            
        Returns:
            float: Implied probability (0-1)
        """
        if not odds:
            return None
            
        if odds > 0:
            return 100 / (odds + 100)
        else:
            return abs(odds) / (abs(odds) + 100)
    
    def __str__(self):
        if not self.raw_data:
            return "No odds data available"
            
        favorite = self.get_favorite()
        underdog = self.get_underdog()
        
        if not favorite or not underdog:
            return "No clear favorite/underdog"
            
        favorite_odds = self.moneyline[favorite]['odds']
        underdog_odds = self.moneyline[underdog]['odds']
        
        spread = self.spread[underdog]['point_spread']
        over_under = self.over_under.get('line', 'N/A')
        
        return (
            f"Spread: {underdog.capitalize()} {spread} ({underdog_odds if underdog_odds > 0 else ''})\n"
            f"Moneyline: {favorite.capitalize()} {favorite_odds if favorite_odds > 0 else ''} | "
            f"{underdog.capitalize()} {underdog_odds if underdog_odds > 0 else ''}\n"
            f"Total: {over_under} (O/U)"
        )