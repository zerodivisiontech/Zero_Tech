from pathlib import Path
import yfinance as yf

DATA_DIR = Path("projects/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def fetch(symbol: str, start: str, out_name: str) -> None:
    print(f"Downloading {symbol} since {start}...")
    df = yf.download(symbol, start=start, progress=False)
    if df.empty:
        raise RuntimeError(f"No data returned for {symbol}.")
    out_path = DATA_DIR / out_name
    df.to_csv(out_path)
    print(f"Saved: {out_path} ({len(df)} rows)")

def main() -> None:
    print("=== CRI: data ingest ===")
    fetch("BTC-USD", "2017-01-01", "btc_usd.csv")
    fetch("ETH-USD", "2017-01-01", "eth_usd.csv")
    fetch("SOL-USD", "2020-01-01", "sol_usd.csv")
    print("Done.")

if __name__ == "__main__":
    main()