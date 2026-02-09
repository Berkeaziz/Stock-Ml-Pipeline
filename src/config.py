import os
from dotenv import load_dotenv

# Airflow container içinde proje buraya mount ediliyor:
PROJECT_ROOT = os.getenv("PROJECT_ROOT", "/opt/airflow/project")
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")

load_dotenv(dotenv_path=ENV_PATH)  

DB_USER = os.getenv("POSTGRES_USER", "berke166")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "depass")
DB_NAME = os.getenv("POSTGRES_DB", "berke_db")
DB_PORT = os.getenv("POSTGRES_PORT", "5435")
DB_HOST = os.getenv("DB_HOST", "host.docker.internal")

ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
SYMBOL = os.getenv("SYMBOL", "IBM")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
