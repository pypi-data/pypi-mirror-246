from pathlib import Path
from importlib import metadata

NAME: str = "cephalon-interface"
VERSION: str = metadata.version(NAME)

HOME = Path.home()
CACHE = HOME / ".ci"
CACHE.mkdir(exist_ok=True)
TOKEN = CACHE / "token.toml"
