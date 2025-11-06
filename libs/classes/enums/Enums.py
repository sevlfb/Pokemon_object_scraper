from enum import Enum

"""
Defaults Enumerations. I think handling multiple languages is way too much effort lmao. It's in ***FRENCH*** 
Enumerating everything here will make it easier for when I will wnant to add multi-lang.
"""

class BadgeOrNameEnum(Enum):
    BADGE = "badge"
    NAME = "name"


class LangEnum(Enum):
    FRENCH = "français"
    ENGLISH = "english"
    

class GameEnum(Enum):
    PLATINUM = "Platinum"
    XY = "XY"
    
    
class ObjectEnum(Enum):
    ITEMS = "items"
    POKEMONS = "pokemons"
    

class HiddenMoves(Enum):
    ROCK_SMASH = "éclate-roc"
    CUT ="coupe"
    STRENGTH = "force"
    FLY = "vol"
    SURF = "surf"
    FLASH = "flash"
    WHIRLPOOL = "siphon"
    WATERFALL = "cascade"
    DIVE = "plongée"
    DEFOG = "anti-brume"
    ROCK_CLIMB = "escalade"
    BIKE = "bicyclette"
    

class ArenaCities(Enum):
    CHARBOURG = "Charbourg"
    

class ZonesEnums(Enum):
    CANNE = "canne"
    SUPER_CANNE = "super canne"
    MEGA_CANNE = "méga canne"
    SURF = "surf"
    
    
    
