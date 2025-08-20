from utilities import request
from .NFLData import NFLData


class Game(NFLData):
    def __init__(self, teams):
        self.teams = teams
    
    @staticmethod
    async def get(gameID):
        # return a Game object

        if not isinstance(gameID, int):
            raise TypeError("GameID must be an int")

        try:
            urls = [
                f"http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{gameID}",
                f"http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{gameID}/competitions/{gameID}/odds"
            ]

            all_data = await request.get(urls)
            return all_data
        except:
            raise