from dotenv import load_dotenv
from pathlib import Path
import os
load_dotenv()

DISCORD_TOKEN = os.environ["TOKEN"]
SUMS_USERNAME = os.environ["SUMS_USER"]
SUMS_PASSWORD = os.environ["SUMS_PASS"]
SUMS_GROUP_ID = os.environ["SUMS_GROUP_ID"]
SELENIUM_URL = os.environ["SELENIUM_URL"]
IGNORED_STUDENT_IDS = set(os.environ["IGNORED_STUDENT_IDS"].split(",")) # set for that sweet O(1)
DISCORD_SV_ID = int(os.environ["DISCORD_SERVER_ID"])
MEMBER_ROLE_ID = int(os.environ["DISCORD_MEMBER_ROLE_ID"])
DB_PATH = Path("data/members.db")