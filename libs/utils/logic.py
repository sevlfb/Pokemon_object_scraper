
from libs.classes.GameLocations.GameLocationsAbstract import GameLocationsAbstract
from .string_utils import str_contains, href_equal_place
import unidecode
from libs.classes.enums.Enums import BadgeOrNameEnum


NOT_FOUND = "Not Found"

def cs_badge_from_string(string, game_enum: GameLocationsAbstract):
    """_summary_

    Args:
        string (_type_): _description_
        game_enum (GameLocations): _description_

    Returns:
        _type_: _description_
    """
    CS_list = [game_enum.hm_dict[cs] for cs in game_enum.hm_dict if str_contains(string, cs.value)]
    if len(CS_list) > 0:
        if len(CS_list) == 1:
            return CS_list[0]
        OU = " ou "
        min_badge = 0
        if OU in string:
            min_badge = min(CS_list)
        else:
            min_badge = max(CS_list)
        return min_badge
    return -1


def change_object(location_badge_discovery: str, object_desc: str, object_name: str, outer_category: str, inner_category: str, url_name_place: str, game_locations: GameLocationsAbstract):
    #print("ok:", location_badge_discovery, object_desc, object_name, outer_category, inner_category, url_name_place,  sep=" | ")
    # ok: | 0 | Au sol en hauteur après le pont | Rappel |  | route_207 |
    location_badge_discovery = int(location_badge_discovery)
    table_desc_city_badge = int(get_badge_for_name_place(outer_category, url_name_place, game_locations))    
    location_sub_badge = int(get_badge_for_name_place(inner_category, url_name_place, game_locations))
    object_badge = cs_badge_from_string(object_desc, game_locations)
    table_desc_badge = cs_badge_from_string(outer_category, game_locations)
    # Mega-Gemmes
    if unidecode.unidecode(object_name).strip().endswith("ite") and all([tmp_text not in object_name.lower() for tmp_text in ["pepite", "insolite"]]):
        return 9
    return max(location_badge_discovery, table_desc_city_badge, table_desc_badge, object_badge, location_sub_badge)



def get_badge_or_name_for_place(place_name: str, return_data: str, game_locations: GameLocationsAbstract):
    return_data = BadgeOrNameEnum(return_data.lower()).value
    # If place name is not translatable -> look in map    
    if place_name in game_locations.locations_map:
        place_name = game_locations.locations_map[place_name]
        
    for badge_unlock in game_locations.locations_order:
        list_places = game_locations.locations_order[badge_unlock]["places"]
        # If place name is well written -> return
        if place_name in list_places:
            return badge_unlock if return_data == "badge" else place_name
        # If place name is not well written -> translate
        if any(places_bool := [href_equal_place(href=place_name, place_name=place) for place in list_places]):
            return badge_unlock if return_data == "badge" else list_places[places_bool.index(True)]
    return -1 if return_data == "badge" else NOT_FOUND


def get_badge_for_name_place(real_place_name: str, url_name_split: str, game_locations: GameLocationsAbstract):
    MONT_COURONNE = "mont_couronne"
    if real_place_name.find(" et ") >= 0:
        real_place_name = real_place_name.split(" ")[-1]
    for badge in game_locations.locations_order:
        if len(real_place_name) > 0 and any([(real_place_name.find(place) >= 0 or (place.find(real_place_name) >= 0 and url_name_split == MONT_COURONNE)) for place in game_locations.locations_order[badge]["places"]]):
            return int(badge)
    return -1


def put_key(dict_:dict=None, value=None, keys: list=[]):
    """Inserts the value in given dict at the path order in keys list, then returns final dict

    Args:
        dict_ (dict, optional): _description_. Defaults to None.
        value (_type_, optional): _description_. Defaults to None.
        keys (list, optional): _description_. Defaults to [].

    Returns:
        _type_: _description_
    """
    if dict_ is None:
        dict_ = {}
    depth = len(keys)
    if depth == 0:
        return value
    if depth == 1:
        if keys[0] in dict_:
            if type(dict_[keys[0]]) == list:
                if type(value) == list:
                    dict_[keys[0]] += value
                else:
                    dict_[keys[0]].append(value)
            else:
                dict_[keys[0]] = value
        else:
            dict_[keys[0]] = value
        return dict_
    if keys[0] in dict_:
        dict_[keys[0]] = put_key(dict_[keys[0]], value, keys[1:])
        return dict_
    else:
        dict_[keys[0]] = {keys[1]: {}}
        dict_[keys[0]][keys[1]] = put_key(dict_[keys[0]][keys[1]], value, keys[2:])
        return dict_