from src.config import ALPHAVANTAGE_API_KEY, SYMBOL, DB_URL
from src.etl.extract import fetch_weekly
from src.etl.transform import to_dataframe
from src.etl.load import upsert_weekly

def main():
    if not ALPHAVANTAGE_API_KEY:
        raise RuntimeError("ALPHAVANTAGE_API_KEY missing. Put it in .env")

    raw = fetch_weekly(SYMBOL, ALPHAVANTAGE_API_KEY)
    df = to_dataframe(raw)
    upsert_weekly(df, DB_URL)

    print(f"Loaded/updated {len(df)} rows for {SYMBOL} into PostgreSQL")

if __name__ == "__main__":
    main()
