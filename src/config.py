import os 
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD =os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_HOST = os.getenv("DB_HOST", "localhost")

ALPHAVANTAGE_API_KEY=os.getenv("ALPHAVANTAGE_API_KEY")
SYMBOL = os.getenv("SYMBOL")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

