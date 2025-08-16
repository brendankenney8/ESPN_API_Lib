# This is an abstract data class which can implemented later with any type of data we want to make available
#  (such as getting stats or teams, etc.)
# Currently only one abstract method
import requests
from abc import ABC, abstractmethod

class NFLData:
    @abstractmethod
    def get():
        pass
