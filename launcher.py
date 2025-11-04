import time
import sys
from lib.utils.bs4_utils import get_soup, get_all_places, get_place_objects, get_badge_or_name_for_place
from lib.utils.excel_utils import write_all_data_in_excel
from lib.classes.GameLocations import PlatinumLocations, XYLocations, GameLocations

NOT_FOUND = 'Not Found'

def main(game_locations: GameLocations.GameLocations):
    deb = time.time()
    
    places_soup = get_soup(game_locations.locations_url, tags=["li"], classes=["listh-bipcode"])
    list_places = get_all_places(places_soup)
        
    global_object_data = {key: {} for key in game_locations.locations_order}
    for i_, place_url in enumerate(list_places):
        print(f"{int(float(i_)/len(list_places)*100)}%", end="\r")
        place_name = place_url.split('/')[-1]
        place_data = get_place_objects(place_url, game_locations)
        for badge_number, objects_data in place_data.items():
            place_to_insert = get_badge_or_name_for_place(place_name, "name", game_locations)
            if place_to_insert != NOT_FOUND:
                #print(f"Correct insertion for {place_name}")
                global_object_data[badge_number][place_to_insert] = objects_data
            else:
                pass
                print(f"{place_name}, {place_to_insert} is not referenced in chronological_order_places")
    
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
            main()
            
        
        if game_name.lower() in ["xy", "x", "y"]:
            game_locations = XYLocations.XYLocations()
            main()
            


