import requests
from bs4 import BeautifulSoup, SoupStrainer, ResultSet, Tag, NavigableString
import requests
import unidecode
from ..classes.GameLocations.GameLocations import GameLocations
from ..classes.enums.Enums import BadgeOrNameEnum

    
URL_PREFIX = "https://www.pokebip.com"
NOT_FOUND = 'Not Found'
SESSION = requests.Session()


def get_place_name(place_url: str) -> str:
    return place_url.split("/")[-1]


def href_equal_place(href: str, place_name: str) -> str:
    return href.split("/")[-1].replace("route0", "route").replace("route", "route_").replace("__", "_").replace("_", " ").replace("-", " ") \
    == unidecode.unidecode(place_name).lower().replace("_", " ").replace("-", " ").replace("'", "")


def get_place_objects(place_url: str, game_locations: GameLocations) -> dict | None:
    TAGS = ["div", "h2", "h3"]
    soup = get_soup(URL_PREFIX+place_url, tags=TAGS)
    if soup is not None:
        object_tables = get_object_tables(soup)
        #print("Number of tables in page:", (len(object_tables)), object_tables)
        place_all_objects = {}
        if len(object_tables) > 0:
            place_all_objects = get_object_table_content(object_tables, get_place_name(place_url), game_locations)
        return place_all_objects
    return None


def str_contains(str_: str, find_: str):
    return str_.find(find_) > -1


def cs_badge_from_string(string, game_enum: GameLocations):
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


def change_object(place_order: str, object_desc: str, object_: str, location_desc: str, url_name_place: str, table_desc_: str, game_locations: GameLocations):
    place_order = int(place_order)
    table_desc_city_badge = int(get_badge_for_name_place(table_desc_, url_name_place, game_locations))    
    location_sub_badge = int(get_badge_for_name_place(location_desc, url_name_place, game_locations))
    object_badge = cs_badge_from_string(object_desc, game_locations)
    table_desc_badge = cs_badge_from_string(table_desc_, game_locations)
    # Mega-Gemmes
    if unidecode.unidecode(object_).strip().endswith("ite") and all([tmp_text not in object_.lower() for tmp_text in ["pépite", "insolite"]]):
        return 9
    return max(place_order, table_desc_city_badge, table_desc_badge, object_badge, location_sub_badge)




def get_soup(url: str, tags: list=[], classes: list=[]) -> BeautifulSoup:
    """Returns a BeautifulSoup of the given URL.

    Args:
        url (str): Internet URL
        tags (list, optional): Specific tags to parse_only. Defaults to [].
        classes (list, optional): Specific classes to parse_only. Defaults to [].

    Returns:
        BeautifulSoup: BeautifulSoup of the given URL, that might have parse_only args.
    """
    r = SESSION.get(url)
    if classes:
        strainer = SoupStrainer(name=tags, attrs={"class": classes})
    else:
        strainer = SoupStrainer(name=tags)
    return BeautifulSoup(r.text, "html.parser", parse_only=strainer)


def get_all_places(soup: BeautifulSoup) -> list[ResultSet]:
    """_summary_

    Args:
        soup (BeautifulSoup): _description_

    Returns:
        list[ResultSet]: _description_
    """
    class_to_get = "listh-bipcode"
    #return [road.find("a")["href"] for list_ in 
    #        soup.find_all(attrs={"class": class_to_get}) 
    #        for road in list_.find_all("strong")]
    return [r["href"] for road in soup.find_all(attrs={"class": class_to_get}) for r in road.find_all("a")]


def find_all_in_text(text: str, *args) -> bool: 
    """Checks if all args are found in a string.

    Args:
        text (str): Text to look in for args

    Returns:
        bool: True if all args are in text, else False 
    """
    found_args = [text.find(arg) > -1 for arg in args]
    return all(found_args)


def find_next_table(object_hook: Tag | NavigableString, tables_: list=[]) -> list[ResultSet]:
    """Returns all next ObjectTable of a page from a hook.

    Args:
        object_hook (Tag | NavigableString): _description_
        tables_ (list, optional): _description_. Defaults to [].

    Returns:
        _type_: _description_
    """
    if (title_hook := object_hook.find_next("h3")) is not None:
        if (table_hook := title_hook.find_next("div", attrs={"class": "table-container"})) and find_all_in_text(table_hook.text, "Img.", "Objet", "Localisation"):
            tables_.append((object_hook.find_next("h3").text, table_hook))
            return find_next_table(table_hook, tables_)
        
    # There is no title before the first table
    if (table_hook := object_hook.find_next("div", attrs={"class": "table-container"})) and find_all_in_text(table_hook.text, "Img.", "Objet", "Localisation"):
        tables_.append(("", table_hook))
        return find_next_table(table_hook, tables_)

    #print("caca")
    return tables_


def get_object_tables(soup: BeautifulSoup) -> list[ResultSet]:
    """Returns all object tables in a page. 'tables' doesn't always initialize to [] due to recursivity so always initialize it outside the function.

    Args:
        soup (BeautifulSoup): BeautifulSoup of a Web URL.

    Returns:
        list[ResultSet]: list of all object tables
    """
    object_hook = soup.find("h2", string="Objets")
    if object_hook is not None:
        tablesA = find_next_table(object_hook, [])
        return tablesA
    return []

    # This is the previous version without recursivity
    #table_titles = object_hook.find_all_next("h3")
    #if len(table_titles) > 0:
    #    return [(table_title.text, table_title.find_next("div", attrs={"class": "table-container"})) for table_title in table_titles if find_all_in_text(table_title.find_next("div", attrs={"class": "table-container"}).text, "Img.", "Objet", "Localisation")]
    #else:
    #    return [("", table) for table in object_hook.find_all_next("div", attrs={"class": "table-container"}) if find_all_in_text(table.text, "Img.", "Objet", "Localisation")]
    
    #class_to_get = "table-container"
    #tables = soup.findAll(attrs = {"class": class_to_get})
    #return [table for table in tables
    #        if find_all_in_text(table.text, "Img.", "Objet", "Localisation")]

 
 
 
def get_badge_or_name_for_place(place_name: str, return_data: str, game_locations: GameLocations):
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


def get_badge_for_name_place(real_place_name, url_name_split, game_locations: GameLocations):
    MONT_COURONNE = "mont_couronne"
    if real_place_name.find(" et ") >= 0:
        real_place_name = real_place_name.split(" ")[-1]
    for badge in game_locations.locations_order:
        if len(real_place_name) > 0 and any([(real_place_name.find(place) >= 0 or (place.find(real_place_name) >= 0 and url_name_split == MONT_COURONNE)) for place in game_locations.locations_order[badge]["places"]]):
            return int(badge)
    return -1



def get_object_table_content(object_tables, place_name, game_locations: GameLocations):
    # Improve, get objects sub_location in <th> like:
    # 1er etage, vers Célestia, ... to divide the objects better
    
    ROW = 'tr'
    CELL = 'td'
    LOCATION = 'th'
    DESCRIPTION_INDEX = -1
    return_data = {}
    for i, (table_desc, table) in enumerate(object_tables):
        LOCATION_DESC = ""
        for row in table.find_all(ROW)[:]:
            row_data = []
            for i, cell in enumerate(row.find_all(CELL)):
                try:
                    cell_value = cell.text if i > 0 else cell.find("img")["src"]
                except:
                    print(place_name, cell)
                row_data.append(cell_value)
            if len(location_desc := row.find_all(LOCATION)) == 1:
                LOCATION_DESC =  location_desc[0].text
            if len(row_data) > 0:
                badge_unlock_for_object = change_object(get_badge_or_name_for_place(place_name, "badge", game_locations),
                            row_data[DESCRIPTION_INDEX], 
                            row_data[-2],
                            LOCATION_DESC, 
                            place_name, 
                            table_desc, 
                            game_locations)
                return_data = put_key(return_data, [row_data], [str(badge_unlock_for_object), table_desc, LOCATION_DESC])
                #if str(badge_unlock_for_object) in return_data:
                 #   if table_desc in return_data[str(badge_unlock_for_object)]:
                  #      if LOCATION_DESC in return_data[str(badge_unlock_for_object)][table_desc]:
                   #         return_data[str(badge_unlock_for_object)][table_desc][LOCATION_DESC].append(row_data)
                    #    else:
                     #       return_data[str(badge_unlock_for_object)][table_desc][LOCATION_DESC] = [row_data]
                  #  else:
                 #       return_data[str(badge_unlock_for_object)][table_desc] = {LOCATION_DESC: [row_data]}
                #else:
               #     return_data[str(badge_unlock_for_object)] = {table_desc: {LOCATION_DESC: [row_data]}}
    return return_data


def put_key(dict_:dict=None, value=None, keys: list=[]):
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
    