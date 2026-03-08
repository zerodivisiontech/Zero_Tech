from pathlib import Path
import pandas as pd

DATA_DIR = Path("projects/data")

def zscore(series, window=365):
    mean = series.rolling(window).mean()
    std = series.rolling(window).std()
    return (series - mean) / std

eth_btc = pd.read_csv(DATA_DIR / "eth_btc.csv", index_col=0, parse_dates=True)
sol_btc = pd.read_csv(DATA_DIR / "sol_btc.csv", index_col=0, parse_dates=True)

eth_z = zscore(eth_btc["eth_btc"])
sol_z = zscore(sol_btc["sol_btc"])

eth_z.to_csv(DATA_DIR / "eth_z.csv", header=["eth_z"])
sol_z.to_csv(DATA_DIR / "sol_z.csv", header=["sol_z"])

print("Z-scores created.")