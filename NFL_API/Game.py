from utilities import request
from utilities.async_utils import run as _run
from .NFLData import NFLData


class Game(NFLData):
    def __init__(self, teams):
        self.teams = teams

    @staticmethod
    def get(gameID):
        """Synchronous API. Runs the async variant under the hood.

        Raises a clear error if called from within a running event loop.
        """
        return _run(Game.get_async(gameID))

    @staticmethod
    async def get_async(gameID):
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