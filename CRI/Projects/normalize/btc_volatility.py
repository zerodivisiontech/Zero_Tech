from pathlib import Path
import pandas as pd

# =========================================================
# BTC VOLATILITY COMPRESSION SENSOR
# Purpose:
# Create a signal where unusually LOW BTC volatility
# becomes a positive value for CRI.
# =========================================================

# ---------------------------------------------------------
# 1. DATA LOCATION
# ---------------------------------------------------------
DATA_DIR = Path("projects/data")

# ---------------------------------------------------------
# 2. LOAD BTC PRICE DATA
# The BTC CSV from yfinance has a 2-row header
# ---------------------------------------------------------
print("Loading BTC price data...")

btc = pd.read_csv(
    DATA_DIR / "btc_usd.csv",
    header=[0, 1],
    index_col=0
)

# Convert index to datetime
btc.index = pd.to_datetime(btc.index, errors="coerce")
btc = btc.sort_index()

# Extract BTC close price
btc_close = btc["Close"].iloc[:, 0]
btc_close = pd.to_numeric(btc_close, errors="coerce").dropna()

# ---------------------------------------------------------
# 3. CALCULATE DAILY RETURNS
# ---------------------------------------------------------
print("Calculating daily returns...")

returns = btc_close.pct_change()

# ---------------------------------------------------------
# 4. CALCULATE 30-DAY ROLLING VOLATILITY
# ---------------------------------------------------------
print("Calculating 30-day rolling volatility...")

vol_30 = returns.rolling(30).std()

# ---------------------------------------------------------
# 5. CALCULATE 365-DAY ROLLING Z-SCORE
# ---------------------------------------------------------
print("Calculating 365-day z-score...")

mean_365 = vol_30.rolling(365).mean()
std_365 = vol_30.rolling(365).std()

vol_z = (vol_30 - mean_365) / std_365

# ---------------------------------------------------------
# 6. INVERT THE SIGNAL
# Low volatility = positive compression signal
# High volatility = negative compression signal
# ---------------------------------------------------------
print("Inverting signal for compression...")

btc_vol_compression_z = -vol_z

# ---------------------------------------------------------
# 7. SAVE OUTPUT
# ---------------------------------------------------------
out = btc_vol_compression_z.dropna().to_frame("btc_vol_compression_z")

out_path = DATA_DIR / "btc_vol_compression_z.csv"
out.to_csv(out_path)

print("Saved:", out_path)
print(out.tail())