"""Configuration module for loading environment variables."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
