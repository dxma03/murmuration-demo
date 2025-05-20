# build_path.py  – run once to create flight.json
import json, requests, datetime as dt, os, pandas as pd, numpy as np

API_KEY = "PASTE-YOUR-KEY-HERE"
TICKERS = ["AAPL", "MSFT", "AMZN"]
START, END = "2020-01-01", "2023-12-31"

def fetch(tk):
    url = f"https://api.polygon.io/v2/aggs/ticker/{tk}/range/1/day/{START}/{END}"
    r = requests.get(url, params=dict(apiKey=API_KEY, adjusted="true", limit=50000))
    rows = r.json()["results"]; return [r["c"] for r in rows]

prices = np.array([fetch(t) for t in TICKERS]).T    # shape (days, N)

# VERY simple 2-D positions: x = cum-return, y = index
pos = (prices / prices[0] - 1) * 10                 # scale nicely
y   = np.arange(len(TICKERS))*2                     # static rows
flight = [[[pos[d,i], y[i]] for i in range(len(TICKERS))]
           for d in range(len(pos))]

with open("flight.json", "w") as f:
    json.dump(dict(pos=flight,
                   dates=[str(dt.date(2020,1,1)+dt.timedelta(d)) for d in range(len(pos))]),
              f)
print("✔︎ wrote flight.json  (keep this next to index.html)")
