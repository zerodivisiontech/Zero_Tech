from pathlib import Path
import requests

print("btc_dominance.py started")

DATA_DIR = Path("projects/data")
print("Data dir:", DATA_DIR.resolve())

url = "https://api.coingecko.com/api/v3/global"
print("Requesting:", url)

r = requests.get(url, timeout=15)
print("Status code:", r.status_code)

data = r.json()
print("Top-level keys:", list(data.keys()))

btc_dom = data["data"]["market_cap_percentage"]["btc"]
print("Current BTC dominance:", btc_dom)

print("btc_dominance.py finished")