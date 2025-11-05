import requests
from bs4 import BeautifulSoup, SoupStrainer, ResultSet, Tag, NavigableString
import requests
import unidecode
from ..classes.GameLocations.GameLocationsAbstract import GameLocationsAbstract
from ..classes.enums.Enums import BadgeOrNameEnum
from .string_utils import get_place_name, find_all_in_text
from .logic import get_badge_or_name_for_place, put_key, change_object

    
URL_PREFIX = "https://www.pokebip.com"
NOT_FOUND = 'Not Found'
SESSION = requests.Session()

def get_location_objects(place_url: str, game_locations: GameLocationsAbstract) -> dict | None:
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



def get_object_table_content(object_tables, place_name, game_locations: GameLocationsAbstract):
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



    