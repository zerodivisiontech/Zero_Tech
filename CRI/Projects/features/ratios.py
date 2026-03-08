from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]   # Z:\CRI
DATA_DIR = ROOT / "projects" / "data"

def load_ohlc(csv_name: str) -> pd.DataFrame:
    path = DATA_DIR / csv_name
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    # Try yfinance multi-header: first row = field names (Open/High/Low/Close/etc)
    # second row = ticker (BTC-USD)
    try:
        df = pd.read_csv(path, header=[0, 1], index_col=0)
        # If this worked, df.columns is a MultiIndex like ('Close','BTC-USD')
        if isinstance(df.columns, pd.MultiIndex):
            # Pick the Close "field" across tickers; result is a DataFrame (one column)
            close = df["Close"]
            # If multiple tickers somehow exist, take the first column
            if hasattr(close, "columns"):
                close_series = close.iloc[:, 0]
            else:
                close_series = close
            close_series.index = pd.to_datetime(close_series.index, errors="coerce")
            close_series = close_series.dropna().sort_index()
            close_series = pd.to_numeric(close_series, errors="coerce").dropna()
            return close_series.to_frame("Close")
    except Exception:
        pass

    # Fallback: normal flat CSV (Date column exists)
    df = pd.read_csv(path)
    # Find date-ish column
    date_col = None
    for cand in ["Date", "Datetime", "Timestamp", "Unnamed: 0"]:
        if cand in df.columns:
            date_col = cand
            break
    if date_col is None:
        raise KeyError(f"No date-like column found in {csv_name}. Columns: {list(df.columns)}")

    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col]).set_index(date_col).sort_index()

    if "Close" not in df.columns:
        raise KeyError(f"'Close' not found in {csv_name}. Columns: {list(df.columns)}")

    out = df[["Close"]].copy()
    out["Close"] = pd.to_numeric(out["Close"], errors="coerce")
    return out.dropna()

def main() -> None:
    btc = load_ohlc("btc_usd.csv")
    eth = load_ohlc("eth_usd.csv")
    sol = load_ohlc("sol_usd.csv")

    # Align by date automatically via index
    eth_btc = (eth["Close"] / btc["Close"]).dropna()
    sol_btc = (sol["Close"] / btc["Close"]).dropna()

    eth_btc.to_csv(DATA_DIR / "eth_btc.csv", header=["eth_btc"])
    sol_btc.to_csv(DATA_DIR / "sol_btc.csv", header=["sol_btc"])

    print("Ratios created:")
    print(" -", DATA_DIR / "eth_btc.csv")
    print(" -", DATA_DIR / "sol_btc.csv")

if __name__ == "__main__":
    main()