from pathlib import Path
import requests
import pandas as pd

# =========================================================
# BTC DOMINANCE HISTORY
# Builds historical BTC dominance using:
# BTC market cap / total crypto market cap * 100
# Source: CoinGecko API
# =========================================================

DATA_DIR = Path("projects/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

API_KEY = "API key geos here" # must have pro account but cri works without it 

headers = {
    "x-cg-demo-api-key": API_KEY
}

GLOBAL_URL = "https://api.coingecko.com/api/v3/global/market_cap_chart"
BTC_URL = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"

DAYS = "max"

# =========================================================
# 1. DOWNLOAD HISTORICAL GLOBAL MARKET CAP
# =========================================================
print("Downloading global market cap history...")
global_resp = requests.get(
    GLOBAL_URL,
    params={"vs_currency": "usd", "days": DAYS},
    headers=headers,
    timeout=30,
)
global_resp.raise_for_status()
global_data = global_resp.json()

global_mcap = pd.DataFrame(
    global_data["market_cap_chart"],
    columns=["timestamp", "total_market_cap_usd"]
)
global_mcap["date"] = pd.to_datetime(global_mcap["timestamp"], unit="ms").dt.normalize()
global_mcap = (
    global_mcap.groupby("date", as_index=False)["total_market_cap_usd"]
    .last()
)

# =========================================================
# 2. DOWNLOAD HISTORICAL BTC MARKET CAP
# =========================================================
print("Downloading BTC market cap history...")
btc_resp = requests.get(
    BTC_URL,
    params={"vs_currency": "usd", "days": DAYS},
    headers=headers,
    timeout=30,
)
btc_resp.raise_for_status()
btc_data = btc_resp.json()

btc_mcap = pd.DataFrame(
    btc_data["market_caps"],
    columns=["timestamp", "btc_market_cap_usd"]
)
btc_mcap["date"] = pd.to_datetime(btc_mcap["timestamp"], unit="ms").dt.normalize()
btc_mcap = (
    btc_mcap.groupby("date", as_index=False)["btc_market_cap_usd"]
    .last()
)

# =========================================================
# 3. COMPUTE BTC DOMINANCE
# =========================================================
print("Computing BTC dominance...")
df = pd.merge(global_mcap, btc_mcap, on="date", how="inner")
df["btc_dominance"] = (df["btc_market_cap_usd"] / df["total_market_cap_usd"]) * 100

out = df[["date", "btc_dominance"]].copy()
out = out.dropna().sort_values("date")

out_path = DATA_DIR / "btc_dominance.csv"
out.to_csv(out_path, index=False)

print("Saved:", out_path)
print(out.tail())