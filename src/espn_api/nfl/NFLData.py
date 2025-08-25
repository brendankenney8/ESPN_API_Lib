# This is an abstract data class which can implemented later with any type of data we want to make available
#  (such as getting stats or teams, etc.)
# Currently only one abstract method

from abc import ABC, abstractmethod
from espn_api.utilities.async_utils import run as _run

class NFLData(ABC):
    @classmethod
    def get(cls, *args, **kwargs):
        return _run(cls._get_async(*args, **kwargs))

    @staticmethod
    @abstractmethod
    async def _get_async(*args, **kwargs):
        pass
