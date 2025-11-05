from libs.classes.GameLocations.GameLocationsAbstract import GameLocationsAbstract
from libs.classes.enums.Enums import HiddenMoves

class PlatinumLocations(GameLocationsAbstract):
    
    def __init__(self):
        
        self._locations_url = "https://www.pokebip.com/page/jeuxvideo/platine/guide_des_lieux/index"
        
        self._hm_dict = {
            HiddenMoves.ROCK_SMASH: 1,
            HiddenMoves.CUT: 2,
            HiddenMoves.BIKE: 2,
            HiddenMoves.DEFOG: 3,
            HiddenMoves.FLY: 4,
            HiddenMoves.SURF: 5,
            HiddenMoves.STRENGTH: 6,
            HiddenMoves.ROCK_CLIMB: 7,
            HiddenMoves.WATERFALL: 8
        }
        
        self._arenas_cities_list = [
            "Départ"
            "Charbourg",
            "Vestigion",
            "Unionpolis",
            "Voilaroc",
            "Verchamps",
            "Joliberges",
            "Frimapic",
            "Rivamar",
            "Ligue Pokémon"
        ]
        
        self._locations_order = {
            "0": {
                "unlocks": [""],
                "places": [
                    "Bonaugure", "Route 201", "Rive Lac Vérité", "Lac Vérité",
                    "Littorella", "Route 202", "Route 219",
                    "Féli-Cité", "Route 203", "Route 204", "Chemin Rocheux", "Route 218", "Entrée Charbourg",
                    "Charbourg", "Route 207", "Mine Charbourg",
                ]
            },
            "1": {
                "unlocks": [1],
                "places": [
                    "Floraville", "Pré Floraville", "Route 205", "Les Eoliennes", "Forêt Vestigion",
                    "Vestigion", "Route 211", "QG Team Galaxie", "Piste Cyclable"
                ]
            },
            "2": {
                "unlocks": [2],
                "places": [
                    "Route 206", "Grotte Revêche", "Mont Couronné", "Route 208", "Batiment Galaxie", "Vieux Château",
                    "Unionpolis", "Square Paisible",
                ]
            },
            "3": {
                "unlocks": [3],
                "places": [
                    "Route 209", "Tour Perdue",
                    "Bonville", "Ruines Bonville", "Route 210", "Route 215", 
                    "Voilaroc", "Tunnel Ruineman(Grotte Ruineman)", "Route 214", "Chemin Source"
                ]
            },
            "4": {
                "unlocks": [4],
                "places": [
                    "Rive Lac Courage", "Route 213",
                    "Verchamps", "Route 212",
                ]
            },
            "5": {
                "unlocks": [5],
                "places": [
                    "Chenal 220", "Route 221", "Grand Marais", "Manoir Pokémon",
                    "Célestia", "Psykokwak", "Forge Fuego",
                    "Joliberges", "Île de fer",
                ]
            }    
            ,
            "6": {
                "unlocks": [6],
                "places": [
                    "Lac Courage", "Route 216", "Route 217", "Ile Pleine Lune",
                    "Frimapic", "Temple Frimapic",
                    "Mont Couronné - Lac Souterrain"
                ]
            },
            "7": {
                "unlocks": [7],
                "places": [
                    "Rive Lac Savoir", "Lac Savoir", "QG de la team Galaxie", "Monde Distorsion", "Route 222", "Source Adieu", "Grotte Retour", "QG Galaxie",
                    "Rivamar", "Chenal 223",
                    "Colonnes Lances",
                    "Lac souterrain"
                    "Mont Couronné - 1er étage", "Mont Couronné - 2ème étage", "Mont Couronné - Extérieur - première partie",
                    "Mont Couronné - Deuxième partie", 
                    "Mont Couronné - 3ème étage, avec la cascade - entrée droite",
                    "Mont Couronné - 3ème étage, avec la cascade - entrée gauche"
                    "Mont Couronné - 4ème étage", "Mont Couronné - 5ème étage",
                    "Mont Couronné - Cave"
                ]
            },
            "8":{
                "unlocks": [8],
                "places": [
                    "Route Victoire",
                    "Ligue Pokémon",
                ]
            },
            # = winning the League
            "9": {
                "unlocks": [""],
                "places": [
                    "Route 224", 
                    "Aire de Combat",
                    "Zone de Combat",
                    "Route 225",
                    "Aire de Survie",
                    "Chenal 226",
                    "Route 227",
                    "Mont Abrupt",
                    "Route 228",
                    "Route 229",
                    "Chenal 230",
                    "Aire de Détente"
                ]
            }
        }
    
        self._locations_map =  {
            "route_220": "Chenal 220",
            "route_223": "Chenal 223",
            "route_226": "Chenal 226",
            "feli-cite": "Féli-Cité",
            "grand_marais_verchamps": "Grand Marais",
            "ile-nouvelle-lune": "Île Nouvellune",
            "batiment_galaxie_voilaroc": "QG Galaxie",
            "grotte_tunnel_ruineman": "Tunnel Ruineman(Grotte Ruineman)",
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