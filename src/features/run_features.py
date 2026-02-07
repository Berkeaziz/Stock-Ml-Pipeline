import pandas as pd
from sqlalchemy import create_engine
from src.config import DB_URL
from src.features.build_features import make_features

def main():
    engine = create_engine(DB_URL)

    df = pd.read_sql(
        "SELECT * FROM weekly_stock_prices ORDER BY date",
        engine
    )

    feat = make_features(df)
    feat.to_csv("features.csv", index=False)
    print(f"features.csv created: {len(feat)} rows")

if __name__ == "__main__":
    main()
