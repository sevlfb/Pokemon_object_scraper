from .ScraperBase import ScraperBase
from libs.classes.GameLocations.GameLocationsAbstract import GameLocationsAbstract
from bs4 import BeautifulSoup, ResultSet, Tag
from libs.utils.logic import put_key
from libs.classes.enums.Enums import ObjectEnum
import re

URL_PREFIX = "https://www.pokebip.com"

class PokebipPokemonsScraper(ScraperBase):
       
    def __init__(self, game_locations: GameLocationsAbstract):
        super().__init__(URL_PREFIX, game_locations)
        self.object_string = "Objets"
        self.list_places = self.get_all_locations(
            self.get_soup(game_locations.locations_url, 
                          tags=["li"], 
                          classes=["listh-bipcode"]), 
            location_tag="a", 
            class_to_get="listh-bipcode")
        self.table_tags=["div", "h2", "h3"]
        self.table_class="table-container"
        self.table_cols = ["Img.", "Pokémon", "Loca.", "Proba", "Niv."]
        self.game_name = self.game_locations.game_name
        self.object_ = ObjectEnum.POKEMONS

    #def get_object_tables(self, soup: BeautifulSoup) -> list[ResultSet]:
    #    """Returns all object tables in a page. 'tables' doesn't always initialize to [] due to recursivity so always initialize it outside the function.
#
    #    Args:
    #        soup (BeautifulSoup): BeautifulSoup of a Web URL.
#
    #    Returns:
    #        list[ResultSet]: list of all object tables
    #    """
    #    object_hook = soup.find(self.table_tags[1], string=self.object_)
    #    if object_hook is not None:
    #        tablesA = self.find_next_table(object_hook, 
    #                                       self.table_tags[0], 
    #                                       self.table_tags[-1], 
    #                                       self.table_class, 
    #                                       [])
    #        return tablesA
    #    return []

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


    def get_cell_text(self, cell):
        # br = space
        # strong
        # <td>18-20<strong><span style="color: #33B8FF;"><sup>X</sup></span></strong><br/>13-15<strong><span style="color: red;"><sup>Y</sup></span></strong></td>
        cell_string = str(cell).replace("<br/>", "\n  ")
        cell_string = re.sub("<[^<>]*>", " ", str(cell_string))
        cell_string = re.sub("[ ]+", " ", cell_string)
        return cell_string.strip()


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
        
        ### For pokemons, data is ["N°", "Img.", "Pokémon", "Loca.", "Proba", "Niv."]
        # only interesting is Img, Pokémon, Proba, Niv
        
        
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
                    # Getting only cols 1, 2, 4, 5
                    if i in [1, 2, 4, 5]:
                        # Get Image or Text
                        try:
                            if i == 1:
                                cell_value = cell.find("img")["src"]
                            if i == 2:
                                cell_value = cell.text + " " + " ".join([img["src"] for img in cell.find_all("img")])
                            if i >= 4:
                                cell_value = self.get_cell_text(cell)
                                #cell_value = cell.text
                            row_data.append(cell_value)
                        except Exception as e:
                            print (repr(e))
                    # Add cell to row dsata
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