import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SITE_URL = os.getenv("SITE_URL")
ALLOWED_GROUP_ID = int(os.getenv("ALLOWED_GROUP_ID", 0))
GROUP_USERNAME = os.getenv("GROUP_USERNAME")
CREATOR_ID = int(os.getenv("CREATOR_ID", 0))