import requests
from NFLData import NFLData
import aiohttp
import asyncio

class Game(NFLData):
    def __init__(self, teams):
        self.teams = teams
    
    
    async def get(self, gameID):
        # return a Game object

        if not isinstance(gameID, int):
            raise TypeError("GameID must be an int")

        try:
            async with aiohttp.ClientSession() as session:
                tasks = [
                    self._get_data(session, f"http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/types/2/weeks/18/events/{gameID}"),
                    self._get_data(session, f"http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/types/2/weeks/18/events/{gameID}/competitions/{gameID}/odds")
                ]

                all_data = await asyncio.gather(*tasks, return_exceptions=True)
                return all_data
        except:
            raise Exception("Unable to fetch data")
        
    
    async def _get_data(self, session, url):
        response = await session.request(url)
        data = await response.json()
        return data