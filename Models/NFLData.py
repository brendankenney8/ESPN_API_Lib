# This is an abstract data class which can implemented later with any type of data we want to make available
#  (such as getting stats or teams, etc.)
# Currently only one abstract method

from abc import ABC, abstractmethod

class NFLData:
    @staticmethod
    @abstractmethod
    def get(self, *args, **kwargs):
        pass
