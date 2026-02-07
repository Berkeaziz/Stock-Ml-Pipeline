import pandas as pd
import psycopg
from psycopg import sql

def upsert_weekly(df: pd.DataFrame, db_url: str):
    """
    Upsert weekly stock data into PostgreSQL using psycopg3.
    """

    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:

            # 1) staging table oluştur
            cur.execute("""
                DROP TABLE IF EXISTS stg_weekly;
                CREATE TEMP TABLE stg_weekly (
                    date DATE,
                    open DOUBLE PRECISION,
                    high DOUBLE PRECISION,
                    low DOUBLE PRECISION,
                    close DOUBLE PRECISION,
                    volume DOUBLE PRECISION
                );
            """)

            # 2) dataframe'i staging'e insert et
            rows = [
                (
                    row.date,
                    row.open,
                    row.high,
                    row.low,
                    row.close,
                    row.volume
                )
                for row in df.itertuples(index=False)
            ]

            insert_sql = """
                INSERT INTO stg_weekly
                (date, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cur.executemany(insert_sql, rows)

            # 3) UPSERT
            cur.execute("""
                INSERT INTO weekly_stock_prices(date, open, high, low, close, volume)
                SELECT date, open, high, low, close, volume
                FROM stg_weekly
                ON CONFLICT (date) DO UPDATE SET
                    open = EXCLUDED.open,
                    high = EXCLUDED.high,
                    low  = EXCLUDED.low,
                    close = EXCLUDED.close,
                    volume = EXCLUDED.volume;
            """)

    print(f"Upsert completed: {len(df)} rows")
