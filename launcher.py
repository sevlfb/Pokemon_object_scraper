import time
import sys
#from libs.utils.bs4_utils import get_soup, get_all_places, get_location_objects, get_badge_or_name_for_place
from libs.utils.excel_utils import write_all_data_in_excel
from libs.classes.GameLocations import PlatinumLocations, XYLocations
from libs.utils.logic import change_object, get_badge_or_name_for_place, put_key
from libs.classes.ScraperStrategy import PokebipItemsScraper, PokebipPokemonsScraper, ScraperBase
from libs.classes.enums.Enums import ObjectEnum
import unidecode

NOT_FOUND = 'Not Found'

def main(scraper: ScraperBase.ScraperBase):
    deb = time.time()
    
    global_object_data = scraper.get_all_data_for_game()        
    
    print("Writing in Excel...")
    
    write_all_data_in_excel(global_object_data, game_locations, scraper.game_name.value, unidecode.unidecode(scraper.object_.value.lower()))
    print(f"Program Performances : {time.time() - deb} s.")


if __name__ == '__main__':
    
    print("Getting Objects Data...")
    
    game_option = ["-g", "--game"]
    game_option_pos = 1
    game_option_value = 2
    object_option = ["-o", "--object"]
    object_option_pos = 3
    object_option_value = 4
    if sys.argv[game_option_pos] in game_option and sys.argv[object_option_pos] in object_option:
        game_name = sys.argv[game_option_value]
        object_type = sys.argv[object_option_value]
        selected_object = object_type
        
        if object_type.lower() in ["pokemon", "p", "poke"]:
            selected_object = ObjectEnum.POKEMONS
            
        if object_type.lower() in ["objet", "o", "obj"]:
            selected_object = ObjectEnum.ITEMS
        
        if selected_object.__class__ != ObjectEnum:
            print("Bad object option")
        else:
            if game_name.lower() in ["p", "plat", "platinum"]:
                game_locations = PlatinumLocations.PlatinumLocations()
                
            if game_name.lower() in ["xy", "x", "y"]:
                game_locations = XYLocations.XYLocations()

                
            if selected_object == ObjectEnum.POKEMONS:
                scraper = PokebipPokemonsScraper.PokebipPokemonsScraper(
                                    game_locations)
            if selected_object == ObjectEnum.ITEMS:
                scraper = PokebipItemsScraper.PokebipItemsScraper(
                                    game_locations)
                
            main(scraper)