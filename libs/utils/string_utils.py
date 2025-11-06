import unidecode

def find_all_in_text(text: str, *args) -> bool: 
    """Checks if all args are found in a string.

    Args:
        text (str): Text to look in for args

    Returns:
        bool: True if all args are in text, else False 
    """
    found_args = [text.find(arg) > -1 for arg in args]
    return all(found_args)


def str_contains(str_: str, find_: str):
    return str_.find(find_) > -1


def get_place_name(place_url: str) -> str:
    return place_url.split("/")[-1]


def href_equal_place(href: str, place_name: str) -> str:
    return href.split("/")[-1].replace("route0", "route").replace("route", "route_").replace("__", "_").replace("_", " ").replace("-", " ") \
    == unidecode.unidecode(place_name).lower().replace("_", " ").replace("-", " ").replace("'", "")


def string_contains_images(cell: str):
    if any([img_ext in cell for img_ext in [".png", ".jpg", ".jpeg"]]):
        return True
    return False


def get_images_objects_in_string(images_string: str):
    images_string = images_string.replace("\n", " ")
    images_string_split = [img for img in  images_string.split(" ") if len(img.strip()) > 1]
    images = [image for image in images_string_split if string_contains_images(image)]
    return images