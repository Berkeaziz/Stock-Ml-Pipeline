import pandas as pd

FEATURES = ["lag_1", "lag_2", "ma_4", "volatility", "return_1"]

def make_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df.sort_values("date", inplace=True)

    # volatility
    df["volatility"] = df["high"] - df["low"]

    # returns
    df["return_1"] = df["close"].pct_change(1)

    # lags
    df["lag_1"] = df["close"].shift(1)
    df["lag_2"] = df["close"].shift(2)

    # moving average
    df["ma_4"] = df["close"].rolling(4).mean()

    # target: next week close
    df["target_next_close"] = df["close"].shift(-1)

    df.dropna(inplace=True)
    return df
