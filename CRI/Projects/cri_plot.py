from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# =========================================================
# CRI PLOT
# - full history chart
# - zoomed last 365 days chart
# - regime shading
# - saved PNGs
# =========================================================

DATA_DIR = Path("projects/data")

ACTIVE_SENSORS = [
    "ETH/BTC z-score",
    "SOL/BTC z-score",
    "BTC volatility compression z-score",
]

print("Plotting CRI with sensors:")
for sensor in ACTIVE_SENSORS:
    print(" -", sensor)

# ---------------------------------------------------------
# LOAD BTC
# ---------------------------------------------------------
btc = pd.read_csv(DATA_DIR / "btc_usd.csv", header=[0, 1], index_col=0)
btc.index = pd.to_datetime(btc.index, errors="coerce")
btc = btc.sort_index()

btc_close_df = btc["Close"]
btc_price = btc_close_df.iloc[:, 0]
btc_price = pd.to_numeric(btc_price, errors="coerce").dropna()

# ---------------------------------------------------------
# LOAD CRI
# ---------------------------------------------------------
cri = pd.read_csv(DATA_DIR / "cri.csv", index_col=0)
cri.index = pd.to_datetime(cri.index, errors="coerce")
cri["cri"] = pd.to_numeric(cri["cri"], errors="coerce")
cri = cri.dropna()

# ---------------------------------------------------------
# ALIGN
# ---------------------------------------------------------
aligned = pd.concat(
    [
        btc_price.rename("btc"),
        cri["cri"]
    ],
    axis=1
).dropna()

print("Aligned rows:", len(aligned))
print("CRI date range:", aligned.index.min(), "to", aligned.index.max())

# ---------------------------------------------------------
# PLOT FUNCTION
# ---------------------------------------------------------
def make_plot(df, title, out_name):
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # BTC line
    ax1.plot(df.index, df["btc"], color="black", label="BTC Price")
    ax1.set_ylabel("BTC Price", color="black")
    ax1.tick_params(axis="y", labelcolor="black")

    # CRI line
    ax2 = ax1.twinx()
    ax2.plot(df.index, df["cri"], color="red", label="CRI")
    ax2.set_ylabel("Capital Rotation Index", color="red")
    ax2.tick_params(axis="y", labelcolor="red")

    # Threshold lines
    ax2.axhline(1, color="green", linestyle="--", alpha=0.4)
    ax2.axhline(-1, color="red", linestyle="--", alpha=0.4)

    # Regime shading
    for date, row in df.iterrows():
        if row["cri"] > 1:
            ax1.axvspan(date, date, color="green", alpha=0.05)
        elif row["cri"] < -1:
            ax1.axvspan(date, date, color="red", alpha=0.05)

    # Legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(DATA_DIR / out_name, dpi=300)
    plt.show()

# ---------------------------------------------------------
# FULL CHART
# ---------------------------------------------------------
make_plot(
    aligned,
    f"BTC Price vs Capital Rotation Index ({len(ACTIVE_SENSORS)} sensors)",
    "cri_chart_full.png"
)

# ---------------------------------------------------------
# LAST 365 DAYS
# ---------------------------------------------------------
zoomed = aligned.tail(365)

make_plot(
    zoomed,
    "BTC Price vs Capital Rotation Index (Last 365 Days)",
    "cri_chart_365d.png"
)