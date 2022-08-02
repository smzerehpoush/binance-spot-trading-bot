from os import getenv

from dotenv import load_dotenv

load_dotenv()

BINANCE_API_KEY = getenv('BINANCE_API_KEY')
BINANCE_SECRET_KEY = getenv('BINANCE_SECRET_KEY')
TELEGRAM_API_KEY = getenv('TELEGRAM_API_KEY')
