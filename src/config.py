from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')

LAT, LON = os.getenv('LAT'), os.getenv('LON')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")