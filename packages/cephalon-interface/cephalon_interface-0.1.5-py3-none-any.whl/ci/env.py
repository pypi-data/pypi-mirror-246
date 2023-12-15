from PIL import Image
from pathlib import Path
from importlib import metadata

PACKAGE_NAME: str = "cephalon-interface"
PACKAGE_NAME_TITLE: str = " ".join(PACKAGE_NAME.split("-")).title()
PACKAGE_VERSION: str = metadata.version(PACKAGE_NAME)

PATH_HOME = Path.home()
PATH_CACHE = PATH_HOME / ".ci"
PATH_CACHE.mkdir(exist_ok=True)
PATH_TOKEN = PATH_CACHE / "token.toml"
PATH_PACKAGE = Path(__file__).parent
PATH_INCLUDE = PATH_PACKAGE / ".include"
PATH_LOGO = PATH_INCLUDE / "logo.png"
PATH_THEME = PATH_INCLUDE / "theme.css"
PATH_APP_ENTRY = PATH_PACKAGE / "app" / "entry.py"


CFG_PAGE_ICON = "🧠"
CFG_LAYOUT = "wide"
CFG_INITIAL_SIDEBAR_STATE = "expanded"


OBJ_LOGO: Image = Image.open(PATH_LOGO)

# todo: replace with pyeio
with open(PATH_THEME) as theme_file:
    OBJ_THEME: str = theme_file.read()
theme_file.close()
