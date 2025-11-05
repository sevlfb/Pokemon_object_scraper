import time
import sys
#from libs.utils.bs4_utils import get_soup, get_all_places, get_location_objects, get_badge_or_name_for_place
from libs.utils.excel_utils import write_all_data_in_excel
from libs.classes.GameLocations import PlatinumLocations, XYLocations
from libs.utils.logic import change_object, get_badge_or_name_for_place, put_key
from libs.classes.ScraperStrategy import PokebipItemsScraper, PokebipPokemonsScraper, ScraperBase

NOT_FOUND = 'Not Found'

def main(scraper: ScraperBase.ScraperBase):
    deb = time.time()
    
    global_object_data = scraper.get_all_data_for_game()        
    
    print("Writing in Excel...")
    
    write_all_data_in_excel(global_object_data, game_locations, "Platinum_objects")
    print(f"Program Performances : {time.time() - deb} s.")


if __name__ == '__main__':
    
    print("Getting Objects Data...")
    
    game_option = ["-g", "--game"]
    game_option_pos = 1
    game_option_value = 2
    if sys.argv[game_option_pos] in game_option:
        game_name = sys.argv[game_option_value]
        
        if game_name.lower() in ["p", "plat", "platinum"]:
            game_locations = PlatinumLocations.PlatinumLocations()
            scraper = PokebipItemsScraper.PokebipItemsScraper(
                                  game_locations)
            main(scraper)
            
        
        if game_name.lower() in ["xy", "x", "y"]:
            game_locations = XYLocations.XYLocations()
            scraper = PokebipItemsScraper.PokebipItemsScraper(
                        game_locations)
            main(scraper)