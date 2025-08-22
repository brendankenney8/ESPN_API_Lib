from espn_api.utilities.async_utils import run as _run
from espn_api.utilities.request import get as get_request
from espn_api.nfl.NFLData import NFLData


class Game(NFLData):
    def __init__(self, teams, score, odds, stats):
        self.teams = teams
        self.score = score
        self.odds  = odds
        self.stats = stats

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

            all_data = await get_request(urls)

            # format all_data here into a Game object

            return all_data
        except:
            raise