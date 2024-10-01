from pathlib import Path
from PIL import Image

# ---- DEFINE FILE DIRECTORIES ----

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR.joinpath("static")
DYNAMIC_DIR = BASE_DIR.joinpath("dynamic")
DATA_DIR = BASE_DIR.joinpath("data")

# ---- END OF FILE DIRECTORIES ----

# ---- DEFINE IMAGE PATHS & ICONS ----

# ICO = Image.open(IMG_DIR.joinpath("3.png"))

# ---- END OF IMAGE PATHS & ICONS ----

# ---- DEFINE API KEYS ----

claude_api_key = ""

# ---- END OF API KEYS ----