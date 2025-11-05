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
            
    global_object_data = {}
    for i_, place_url in enumerate(scraper.list_places):
        print(f"{int(float(i_)/len(scraper.list_places)*100)}%", end="\r")
        place_name = place_url.split('/')[-1]
        place_data = scraper.get_location_data(place_url)
        #print(badge_number, items)
        place_to_insert = get_badge_or_name_for_place(place_name, "name", game_locations)
        for outer_category, _ in place_data.items():
            #print(_)
            for inner_category, objects_data in _.items():
                for object_ in objects_data:
                    # object_data = [img, name, desc]
                    # ok: | 0 | Au sol en hauteur après le pont | Rappel |  | route_207 |
                    badge_unlock_for_object = change_object(
                        location_badge_discovery=get_badge_or_name_for_place(place_name, "badge", game_locations),
                        object_desc=object_[-1], 
                        object_name=object_[-2],
                        inner_category=inner_category, 
                        outer_category=outer_category, 
                        url_name_place=place_url, 
                        game_locations=game_locations
                        )
                    global_object_data = put_key(
                        dict_=global_object_data, 
                        value=[object_], 
                        keys=[str(badge_unlock_for_object), place_to_insert, outer_category, inner_category]
                        )
        if place_to_insert != NOT_FOUND:
            pass
            #print(f"Correct insertion for {place_name}")
            #global_object_data[badge_number][place_to_insert] = objects_data
        else:
            pass
            print(f"{place_name} is not referenced in : chronological_order_places")
    
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