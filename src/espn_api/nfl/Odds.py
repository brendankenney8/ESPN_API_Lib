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
    
    def _get_nested_value(self, data, *keys, default=None):
        """Safely get a value from nested dictionaries"""
        current = data
        for key in keys:
            if not isinstance(current, dict):
                return default
            current = current.get(key, {})
        return current if current != {} else default

    def _parse_odds_details(self, odds_data):
        """Parse the main odds details"""
        if not odds_data or not isinstance(odds_data, dict):
            return {}
            
        # Safely get nested dictionaries with defaults
        away_team_odds = self._get_nested_value(odds_data, 'awayTeamOdds', default={})
        home_team_odds = self._get_nested_value(odds_data, 'homeTeamOdds', default={})
        current_data = self._get_nested_value(odds_data, 'current', default={})
        
        # Get current spread values
        current_spread = self._get_nested_value(current_data, 'pointSpread', 'alternateDisplayValue')
        current_total = self._get_nested_value(current_data, 'total', 'alternateDisplayValue')
        
        # Get current moneyline odds
        current_ml_away = self._get_nested_value(away_team_odds, 'current', 'moneyLine', 'american')
        current_ml_home = self._get_nested_value(home_team_odds, 'current', 'moneyLine', 'american')
        
        # Get current spread odds
        current_spread_away = self._get_nested_value(away_team_odds, 'current', 'spread', 'american')
        current_spread_home = self._get_nested_value(home_team_odds, 'current', 'spread', 'american')
        
        # Create details dictionary with type conversion and validation
        details = {
            'details': odds_data.get('details'),
            'over_under': self._safe_float(odds_data.get('overUnder')),
            'over_odds': self._safe_float(odds_data.get('overOdds')),
            'under_odds': self._safe_float(odds_data.get('underOdds')),
            'spread': self._safe_float(odds_data.get('spread')),
            'current_spread': self._safe_float(current_spread) if current_spread else None,
            'current_total': self._safe_float(current_total) if current_total else None,
            'away_team_odds': {
                'favorite': away_team_odds.get('favorite'),
                'underdog': away_team_odds.get('underdog'),
                'money_line': self._safe_int(away_team_odds.get('moneyLine')),
                'current_money_line': self._safe_int(current_ml_away) if current_ml_away else None,
                'spread_odds': self._safe_float(away_team_odds.get('spreadOdds')),
                'current_spread_odds': self._safe_int(current_spread_away) if current_spread_away else None
            },
            'home_team_odds': {
                'favorite': home_team_odds.get('favorite'),
                'underdog': home_team_odds.get('underdog'),
                'money_line': self._safe_int(home_team_odds.get('moneyLine')),
                'current_money_line': self._safe_int(current_ml_home) if current_ml_home else None,
                'spread_odds': self._safe_float(home_team_odds.get('spreadOdds')),
                'current_spread_odds': self._safe_int(current_spread_home) if current_spread_home else None
            },
            'last_updated': odds_data.get('lastUpdated')
        }
        
        # Remove None values
        return {k: v for k, v in details.items() if v is not None}
    
    def _parse_spread(self, odds_data):
        """Parse spread data"""
        if not odds_data or not isinstance(odds_data, dict):
            return {}
            
        away_team_odds = self._get_nested_value(odds_data, 'awayTeamOdds', default={})
        home_team_odds = self._get_nested_value(odds_data, 'homeTeamOdds', default={})
        
        # Get current spread values
        current_spread = self._get_nested_value(odds_data, 'current', 'pointSpread', 'alternateDisplayValue')
        current_spread_away = self._get_nested_value(away_team_odds, 'current', 'pointSpread', 'alternateDisplayValue')
        current_spread_home = self._get_nested_value(home_team_odds, 'current', 'pointSpread', 'alternateDisplayValue')
        
        # Get current spread odds
        current_spread_odds_away = self._get_nested_value(away_team_odds, 'current', 'spread', 'american')
        current_spread_odds_home = self._get_nested_value(home_team_odds, 'current', 'spread', 'american')
        
        spread_data = {
            'away': {
                'point_spread': self._safe_float(odds_data.get('spread')),
                'current_point_spread': self._safe_float(current_spread_away) if current_spread_away else None,
                'spread_odds': self._safe_float(away_team_odds.get('spreadOdds')),
                'current_spread_odds': self._safe_int(current_spread_odds_away) if current_spread_odds_away else None,
                'favorite': away_team_odds.get('favorite'),
                'underdog': away_team_odds.get('underdog')
            },
            'home': {
                'point_spread': self._safe_float(odds_data.get('spread')),
                'current_point_spread': self._safe_float(current_spread_home) if current_spread_home else None,
                'spread_odds': self._safe_float(home_team_odds.get('spreadOdds')),
                'current_spread_odds': self._safe_int(current_spread_odds_home) if current_spread_odds_home else None,
                'favorite': home_team_odds.get('favorite'),
                'underdog': home_team_odds.get('underdog')
            },
            'current_spread': self._safe_float(current_spread) if current_spread else None
        }
        
        # Clean up None values
        return {
            'away': {k: v for k, v in spread_data['away'].items() if v is not None},
            'home': {k: v for k, v in spread_data['home'].items() if v is not None},
            'current_spread': spread_data['current_spread']
        }
    
    def _parse_moneyline(self, odds_data):
        """Parse moneyline data"""
        if not odds_data or not isinstance(odds_data, dict):
            return {}
            
        # Safely get nested data
        away_team_odds = self._get_nested_value(odds_data, 'awayTeamOdds', default={})
        home_team_odds = self._get_nested_value(odds_data, 'homeTeamOdds', default={})
        
        # Get current moneyline odds
        current_ml_away = self._get_nested_value(away_team_odds, 'current', 'moneyLine', 'american')
        current_ml_home = self._get_nested_value(home_team_odds, 'current', 'moneyLine', 'american')
        
        moneyline_data = {
            'away': {
                'odds': self._safe_int(odds_data.get('moneyLineAway')),
                'current_odds': self._safe_int(current_ml_away) if current_ml_away else None,
                'favorite': away_team_odds.get('favorite'),
                'underdog': away_team_odds.get('underdog')
            },
            'home': {
                'odds': self._safe_int(odds_data.get('moneyLineHome')),
                'current_odds': self._safe_int(current_ml_home) if current_ml_home else None,
                'favorite': home_team_odds.get('favorite'),
                'underdog': home_team_odds.get('underdog')
            },
            'draw': {
                'odds': self._safe_int(odds_data.get('moneyLineDraw'))
            }
        }
        
        # Clean up None values
        return {
            'away': {k: v for k, v in moneyline_data['away'].items() if v is not None},
            'home': {k: v for k, v in moneyline_data['home'].items() if v is not None},
            'draw': {k: v for k, v in moneyline_data['draw'].items() if v is not None}
        }
    
    def _safe_float(self, value):
        """Safely convert value to float, return None if not possible"""
        try:
            return float(value) if value is not None else None
        except (ValueError, TypeError):
            return None
            
    def _safe_int(self, value):
        """Safely convert value to int, return None if not possible"""
        try:
            return int(value) if value is not None else None
        except (ValueError, TypeError):
            return None
            
    def _parse_over_under(self, odds_data):
        """Parse over/under data"""
        if not odds_data or not isinstance(odds_data, dict):
            return {}
            
        # Get current over/under data
        current = self._get_nested_value(odds_data, 'current', default={})
        current_over = self._get_nested_value(current, 'over', 'american')
        current_under = self._get_nested_value(current, 'under', 'american')
        current_total = self._get_nested_value(current, 'total', 'alternateDisplayValue')
        
        over_under_data = {
            'line': self._safe_float(odds_data.get('overUnder')),
            'current_line': self._safe_float(current_total) if current_total else None,
            'over_odds': self._safe_float(odds_data.get('overOdds')),
            'current_over_odds': self._safe_int(current_over) if current_over else None,
            'under_odds': self._safe_float(odds_data.get('underOdds')),
            'current_under_odds': self._safe_int(current_under) if current_under else None
        }
        
        # Remove None values
        return {k: v for k, v in over_under_data.items() if v is not None}
    
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