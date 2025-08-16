import requests
from NFLData import NFLData

class Game(NFLData):
    def __init__(self, teams):
        self.teams = teams
    
    
    def get(self, gameID):
        # return a Game object
        return