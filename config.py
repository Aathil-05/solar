import os
from dotenv import load_dotenv

load_dotenv()  # loads .env file

OPENWEATHER_BASE_URL = os.getenv("OPENWEATHER_BASE_URL")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not OPENWEATHER_BASE_URL or not OPENWEATHER_API_KEY:
    raise RuntimeError("❌ OpenWeather environment variables not set")
