from libs.classes.GameLocations.GameLocationsAbstract import GameLocationsAbstract
from libs.classes.enums.Enums import HiddenMoves

class XYLocations(GameLocationsAbstract):
    
    def __init__(self):
        
        self._locations_url = "https://www.pokebip.com/page/jeuxvideo/pokemon-x-y/guide_des_lieux/index"

        
        self._hm_dict = {
            HiddenMoves.ROCK_SMASH: 2,
            HiddenMoves.CUT: 1,
            HiddenMoves.BIKE: 2,
            HiddenMoves.FLY: 4,
            HiddenMoves.SURF: 3,
            HiddenMoves.STRENGTH: 2,
            HiddenMoves.WATERFALL: 8
        }
        
        self._arenas_cities_list = [
            "Départ"
            "Neuvartault",
            "Relifac-Le-Haut",
            "Yantreizh",
            "Port Tempères",
            "Illumis",
            "Romant-Sous-Bois",
            "Flusselles",
            "Auffrac-les-Congères",
            "Ligue Pokémon"
        ]
        
        self._locations_order = {
            "0": {
                "unlocks": [""],
                "places": [
                    "Bourg Croquis", "Route 1",
                    "Quarellis", "Route 2", "Forêt de Neuvartault", "Route 3",
                    "Neuvartault", "Route 22",
                ]
            },
            "1": {
                "unlocks": [1],
                "places": [
                    "Route 4", 
                    "Illumis", "Route 5", 
                    "Fort-Vanitas", "Route 6", "Palais Chaydeuvre", "Route 7",  "Château de Combat", "Cave Connecterre", "Route 8",
                    "Roche-sur-Gliffe", "Route 9", "Grotte Etincelante", "Relifac-le-Haut"
                ]
            },
            "2": {
                "unlocks": [2],
                "places": [
                    "Route 10", "Cromlac'h", "Route 11", "Grotte Miroitante",
                    "Yantreizh", "Route 12"
                ]
            },
            "3": {
                "unlocks": [3],
                "places": [
                    "Baie Azur", 
                    "Antre Néréen",
                    "Port Tempères"
                ]
            },
            "4": {
                "unlocks": [4],
                "places": [
                    "Route 13", "Centrale de Kalos",
                    "Illumis2"
                ]
            },
            "5": {
                "unlocks": [5],
                "places": [
                    "Route 14",
                    "Romant-sous-Bois", "Usine de Poké Balls"
                ]
            }    
            ,
            "6": {
                "unlocks": [6],
                "places": [
                    "Route 15", "Route 16", "Hôtel Désolation",
                    "La Frescale", "Caverne Gelée", "Route 17",
                    "Flusselles", 
                ]
            },
            "7": {
                "unlocks": [7],
                "places": [
                    "Route 18", "Grotte Coda",
                    "Mozheim", "Route 19", 
                    "Auffrac-les-Congères", "Route 20", "Village Pokémon", "Grotte Inconnue"
                ]
            },
            "8":{
                "unlocks": [8],
                "places": [
                    "Labos Lysandre",
                    "Repaire Team Flare",
                    "Route 21",
                    "Route Victoire", "Ligue Pokémon", "Chambre du Néant"
                ]
            },
            # = winning the League
            "9": {
                "unlocks": [""],
                "places": [
                    "Batisques"
                ]
            }
        }
    
        self._locations_map =  {
            "bourg_croquis": "Bourg Croquis",
            "foretneuvartault": "Forêt de Neuvartault",
            "usine_poke_balls": "Usine de Poké Balls"
      }
    
    @property
    def hm_dict(self) -> dict:
        return self._hm_dict
    
    @property
    def arena_cities_list(self) -> list:
        return self._arenas_cities_list
    
    @property
    def locations_order(self) -> dict:
        return self._locations_order
    
    @property
    def locations_map(self) -> dict:
        return self._locations_map
    
    @property
    def locations_url(self) -> dict:
        return self._locations_url
    
    def arena_string(self, index):
        if index == 0:
                return "Départ"
        if index == 9:
                return "Après la Ligue Pokémon"
        return str("Après l'arène de "+self.arena_cities_list[index])[:31]