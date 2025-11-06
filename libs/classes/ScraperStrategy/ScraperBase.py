import requests
from libs.classes.GameLocations.GameLocationsAbstract import GameLocationsAbstract
from libs.utils.string_utils import find_all_in_text
import requests
from bs4 import BeautifulSoup, SoupStrainer, ResultSet, Tag, NavigableString
import requests
from libs.utils.logic import change_object, put_key, get_badge_or_name_for_place
import json

class ScraperBase():
    
    def __init__(self, url_prefix, game_locations: GameLocationsAbstract):
        self.url_prefix = url_prefix
        self.NOT_FOUND = 'Not Found'
        self.session = requests.Session()
        self.game_locations = game_locations

    
    def get_location_data(self, location_url: str) -> dict | None:
        # To override
        #TAGS = ["div", "h2", "h3"]
        soup = self.get_soup(self.url_prefix+location_url, tags=self.table_tags)
        if soup is not None:
            object_tables = self.get_object_tables(soup)
            #print("Number of tables in page:", (len(object_tables)), object_tables)
            place_all_objects = {}
            if len(object_tables) > 0:
                #print(location_url)
                place_all_objects = self.transform_data_table(object_tables)                
            return place_all_objects
        return None


    
    def get_soup(self, url: str, tags: list=[], classes: list=[]) -> BeautifulSoup:
        """Returns a BeautifulSoup of the given URL.

        Args:
            url (str): Internet URL
            tags (list, optional): Specific tags to parse_only. Defaults to [].
            classes (list, optional): Specific classes to parse_only. Defaults to [].

        Returns:
            BeautifulSoup: BeautifulSoup of the given URL, that might have parse_only args.
        """
        r = self.session.get(url)
        if classes:
            strainer = SoupStrainer(name=tags, attrs={"class": classes})
        else:
            strainer = SoupStrainer(name=tags)
        return BeautifulSoup(r.text, "html.parser", parse_only=strainer)


    def get_all_locations(self, soup: BeautifulSoup, location_tag: str, class_to_get: str) -> list[ResultSet]:
        """_summary_

        Args:
            soup (BeautifulSoup): _description_

        Returns:
            list[ResultSet]: _description_
        """
        #return [road.find("a")["href"] for list_ in 
        #        soup.find_all(attrs={"class": class_to_get}) 
        #        for road in list_.find_all("strong")]
        return [r["href"] for road in soup.find_all(attrs={"class": class_to_get}) for r in road.find_all(location_tag)]



    def find_next_table(self, object_hook: Tag | NavigableString, upper_table_tag, sub_table_tag, table_class, tables_: list=[]) -> list[ResultSet]:
        """Returns all next ObjectTable of a page from a hook.

        Args:
            object_hook (Tag | NavigableString): _description_
            tables_ (list, optional): _description_. Defaults to [].

        Returns:
            _type_: _description_
        """
        if (title_hook := object_hook.find_next(sub_table_tag)) is not None:
            if (table_hook := title_hook.find_next(upper_table_tag, attrs={"class": table_class})) and find_all_in_text(table_hook.text, *self.table_cols):
                tables_.append((object_hook.find_next(sub_table_tag).text, table_hook))
                return self.find_next_table(table_hook, upper_table_tag, sub_table_tag, table_class, tables_)
            
        # There is no title before the first table
        if (table_hook := object_hook.find_next(upper_table_tag, attrs={"class": table_class})) and find_all_in_text(table_hook.text, *self.table_cols):
            tables_.append(("", table_hook))
            return self.find_next_table(table_hook, upper_table_tag, sub_table_tag, table_class, tables_)

        return tables_


    def get_object_tables(self, soup: BeautifulSoup, table_tag: str) -> list[ResultSet]:
        """Returns all object tables in a page. 'tables' doesn't always initialize to [] due to recursivity so always initialize it outside the function.

        Args:
            soup (BeautifulSoup): BeautifulSoup of a Web URL.

        Returns:
            list[ResultSet]: list of all object tables
        """
        object_hook = soup.find(table_tag, string="Objets")
        if object_hook is not None:
            tablesA = self.find_next_table(object_hook, [])
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



    def transform_data_table(self, object_tables: dict[str, list[tuple[str, Tag]]]):
        # Improve, get objects sub_location in <th> like:
        # 1er etage, vers Célestia, ... to divide the objects better
        """Transforms the data table from html soup format for 1 location to organized dict

        Args:
            object_tables (list[tuple[str, Tag]]]): the table for 1 locations with html contetn
            location_name (_type_): The name of that location

        Returns:
            _type_: _description_
        """
        
        ROW = 'tr'
        CELL = 'td'
        LOCATION = 'th'
        DESCRIPTION_INDEX = -1
        return_data = {}
        # For every data table in a specific zone
        # iterator, (key=Table sublocation, value=Table Soup)
        for i, (table_outer_category, table) in enumerate(object_tables):
            # If table has multiple categories
            INNER_CATEGORY = ""
            # For every row / object in a table
            for row in table.find_all(ROW)[:]:
                row_data = []
                # For every cell in that row
                for i, cell in enumerate(row.find_all(CELL)):
                    # Get Image or Text
                    try:
                        cell_value = cell.text if i > 0 else cell.find("img")["src"]
                    except:
                        print(cell)
                    # Add cell to row data
                    row_data.append(cell_value)
                # Check if the row has a location description
                if len(location_desc := row.find_all(LOCATION)) == 1:
                    INNER_CATEGORY =  location_desc[0].text
                
                if len(row_data) > 0:
                    return_data = put_key(return_data, value=[row_data], keys=[table_outer_category, INNER_CATEGORY])
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
    
    
    def get_all_data_for_game(self):
        global_object_data = {key: {} for key in self.game_locations.locations_order}
        for i_, place_url in enumerate(self.list_places):
            print(f"{int(float(i_)/len(self.list_places)*100)}%", end="\r")
            place_name = place_url.split('/')[-1]
            place_data = self.get_location_data(place_url)
            #print(badge_number, items)
            place_to_insert = get_badge_or_name_for_place(place_name, "name", self.game_locations)
            for outer_category, _ in place_data.items():
                #print(_)
                for inner_category, objects_data in _.items():
                    for object_ in objects_data:
                        # object_data = [img, name, desc]
                        # ok: | 0 | Au sol en hauteur après le pont | Rappel |  | route_207 |
                        badge_unlock_for_object = change_object(
                            location_badge_discovery=get_badge_or_name_for_place(place_name, "badge", self.game_locations),
                            object_desc=object_[-1], 
                            object_name=object_[-2],
                            inner_category=inner_category, 
                            outer_category=outer_category, 
                            url_name_place=place_url, 
                            game_locations=self.game_locations
                            )
                        global_object_data = put_key(
                            dict_=global_object_data, 
                            value=[object_], 
                            keys=[str(badge_unlock_for_object), place_to_insert, outer_category, inner_category]
                            )
            if place_to_insert != self.NOT_FOUND:
                pass
                #print(f"Correct insertion for {place_name}")
                #global_object_data[badge_number][place_to_insert] = objects_data
            else:
                pass
                print(f"{place_name} is not referenced in : chronological_order_places")        
        #with open("./global_object_data.json", "w") as f:
        #    json.dump(global_object_data, f)
        return global_object_data