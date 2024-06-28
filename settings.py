import os
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv('BOT_TOKEN')
PREFIX = os.getenv('BOT_PREFIX')
EMBED_COLOR = 0x181825
