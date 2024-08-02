import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
RAPIDAPI_HOST = "social-media-video-downloader.p.rapidapi.com"
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
