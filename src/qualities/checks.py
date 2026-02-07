import psycopg

def run_quality_checks(db_url: str) -> None:
    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            # 1) row count
            cur.execute("SELECT COUNT(*) FROM weekly_stock_prices;")
            (cnt,) = cur.fetchone()
            if cnt == 0:
                raise RuntimeError("Quality check failed: table is empty")
            print(f"✅ row_count: {cnt}")

            # 2) null checks
            cur.execute("""
                SELECT
                    SUM(CASE WHEN date IS NULL THEN 1 ELSE 0 END) AS null_date,
                    SUM(CASE WHEN close IS NULL THEN 1 ELSE 0 END) AS null_close
                FROM weekly_stock_prices;
            """)
            null_date, null_close = cur.fetchone()
            if null_date != 0:
                raise RuntimeError(f"Quality check failed: null date = {null_date}")
            if null_close != 0:
                raise RuntimeError(f"Quality check failed: null close = {null_close}")
            print("null_checks: OK")

            # 3) duplicate date check 
            cur.execute("""
                SELECT COUNT(*) - COUNT(DISTINCT date) AS dup_dates
                FROM weekly_stock_prices;
            """)
            (dup_dates,) = cur.fetchone()
            if dup_dates != 0:
                raise RuntimeError(f"Quality check failed: duplicate dates = {dup_dates}")
            print("duplicate_check: OK")
