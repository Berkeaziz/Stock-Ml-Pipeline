import pandas as pd 

def to_dataframe(weekly_dict:dict)->pd.DataFrame:
    df=pd.DataFrame.from_dict(weekly_dict,orient="index").reset_index()
    df.rename(columns={"index":"date"},inplace=True)

    df.columns =["date","open","high","low","close","volume"]

    df["date"] = pd.to_datetime(df["date"]).dt.date
    for c in ["open","high","low","close","volume"]:
        df[c] =df[c].astype(float)
    df.sort_values("date",inplace=True)
    return df