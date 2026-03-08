# Capital Rotation Index (CRI)

This is a small research tool for watching how money moves around the crypto market.

Instead of trying to predict price, CRI looks at **capital rotation** between Bitcoin and major altcoins.

Sometimes the market piles into BTC.  
Sometimes liquidity spreads out into alts.

CRI tries to measure that shift.

This is not a trading bot and it's not financial advice.  
It's just a lens for looking at market structure.

---

## Signals Used

The current version combines a few simple signals:

- ETH/BTC trend
- SOL/BTC momentum
- BTC volatility compression
- BTC dominance movement

Each signal is normalized using a rolling **z-score** so they can be compared on the same scale.

Those signals are averaged into the **Capital Rotation Index (CRI)**.

---

## How To Read It

General guide:

CRI > 1  
Altcoin expansion phase

CRI between -1 and 1  
Mixed / transition market

CRI < -1  
Bitcoin dominance phase

The index is meant to show **market regime**, not exact buy or sell signals.

There is more ifo on this in CRI_docs.

---

## Setup

Create a virtual environment:

python -m venv .venv

Activate it:

.\.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

---

## Run

From inside the CRI folder:

python projects/regime/cri_plot.py

The script generates a chart showing BTC price and the CRI regime index.

---

## Notes

This is an open project.

If you want to experiment with different signals or improve the model, fork it and build on it.