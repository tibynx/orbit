import os
from dotenv import load_dotenv

load_dotenv()

# Set bot token and prefix
TOKEN = os.getenv('BOT_TOKEN')
PREFIX = os.getenv('BOT_PREFIX')

# Set embed color
# Default to Discord blue if not set
EMBED_COLOR = int(os.getenv('BOT_COLOR'), 16) if os.getenv('BOT_COLOR') else 0x7289DA
