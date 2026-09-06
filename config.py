from dotenv import load_dotenv
from pathlib import Path
import os
load_dotenv()

DISCORD_TOKEN = os.environ["TOKEN"]
SUMS_USERNAME = os.environ["SUMS_USER"]
SUMS_PASSWORD = os.environ["SUMS_PASS"]
DISCORD_SV_ID = os.environ["DISCORD_SERVER_ID"]
DB_PATH = Path("data/members.db")