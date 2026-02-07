import requests

API_URL ="https://www.alphavantage.co/query"

def fetch_weekly(symbol:str,api_key:str)->dict:
    params = {
        "function": "TIME_SERIES_WEEKLY", 
        "symbol": symbol, 
        "apikey": api_key
    }
    r = requests.get(API_URL, params=params, timeout=30)
    r.raise_for_status()
    data=r.json()
 
    if "Weekly Time Series" not in data:
        raise ValueError(f"Unexpected API response: {data}")
   
    return data["Weekly Time Series"]
    