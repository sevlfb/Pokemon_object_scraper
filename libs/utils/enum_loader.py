from libs.classes.enums.LangEnums import FrenchEnums
from libs.classes.enums.Enums import LangEnum

def load_enums(lang_enum: LangEnum):
    if lang_enum == LangEnum.FRENCH:
        return FrenchEnums