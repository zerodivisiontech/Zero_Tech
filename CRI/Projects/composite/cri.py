from pathlib import Path
import pandas as pd

# =========================================================
# CAPITAL ROTATION INDEX (CRI)
# Sensors:
# 1. ETH/BTC strength
# 2. SOL/BTC strength
# 3. BTC volatility compression
# =========================================================

DATA_DIR = Path("projects/data")

print("Loading sensors...")

eth_z = pd.read_csv(DATA_DIR / "eth_z.csv", index_col=0, parse_dates=True)
sol_z = pd.read_csv(DATA_DIR / "sol_z.csv", index_col=0, parse_dates=True)
btc_vol = pd.read_csv(DATA_DIR / "btc_vol_compression_z.csv", index_col=0, parse_dates=True)

# ---------------------------------------------------------
# ALIGN DATA BY DATE
# ---------------------------------------------------------
print("Aligning data...")

df = pd.concat([eth_z, sol_z, btc_vol], axis=1)

# ---------------------------------------------------------
# BUILD COMPOSITE INDEX
# ---------------------------------------------------------
print("Computing composite...")

df["cri_raw"] = df.mean(axis=1)

# Smooth signal slightly
df["cri"] = df["cri_raw"].rolling(7).mean()

# ---------------------------------------------------------
# SAVE OUTPUT
# ---------------------------------------------------------
out = df[["cri"]].dropna()

out_path = DATA_DIR / "cri.csv"
out.to_csv(out_path)

print("CRI created.")
print(out.tail())