import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_PREFIX = os.getenv('BOT_PREFIX')
EMBED_COLOR = int(os.getenv('EMBED_COLOR'), 16) if os.getenv('EMBED_COLOR') else 0x7289DA
