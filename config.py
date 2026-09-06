from dotenv import load_dotenv
from pathlib import Path
import os
load_dotenv()

DISCORD_TOKEN = os.environ["TOKEN"]
SUMS_USERNAME = os.environ["SUMS_USER"]
SUMS_PASSWORD = os.environ["SUMS_PASS"]
DB_PATH = Path("data/members.db")