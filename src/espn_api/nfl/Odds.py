from espn_api.utilities.async_utils import run as _run
from espn_api.utilities.request import get as get_request
from espn_api.nfl.NFLData import NFLData

class Odds(NFLData):
    def __init__(self):
        self.test = 0
    
    @staticmethod
    async def get_async():
        return