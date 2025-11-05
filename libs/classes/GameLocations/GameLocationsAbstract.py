from abc import ABC, abstractmethod

class GameLocationsAbstract(ABC):
    
    @property
    @abstractmethod
    def hm_dict(self) -> dict:
        # Hidden Moves and associated badge
        pass

    @property
    @abstractmethod
    def arena_cities_list(self) -> list:
        # List of arena cities in chronological order
        pass
    
    @property
    @abstractmethod
    def locations_order(self) -> dict:
        # All locations sorted by availability through badge award
        pass
    
    @property
    @abstractmethod
    def locations_map(self) -> dict:
        # Locations that have URL and Writting differences
        pass
    
    @property
    @abstractmethod
    def locations_url(self) -> str:
        pass