Capital Rotation Index (CRI)
=============================

Purpose
-------
CRI measures how capital is rotating inside the crypto market.
It does NOT predict price. It measures market regime pressure.

Concept
-------
Instead of looking at price directly, CRI observes how altcoins
perform relative to Bitcoin.

If altcoins are gaining strength vs BTC → capital is rotating outward.
If altcoins are weakening vs BTC → capital is rotating back to BTC.

Current Sensors (v1)
--------------------
1. ETH/BTC relative strength (z-score)
2. SOL/BTC relative strength (z-score)

Each signal is normalized using a rolling 1-year z-score.

Calculation
-----------

Step 1: Align signals by date

    df = pd.concat([eth_z, sol_z], axis=1)

Example table:

Date        ETH_Z    SOL_Z
2021-01-01   0.3      0.5
2021-01-02  -0.2      0.1


Step 2: Equal-weight composite

    df["cri_raw"] = df.mean(axis=1)

Example:

ETH_Z = 0.3
SOL_Z = 0.5

CRI_RAW = (0.3 + 0.5) / 2 = 0.4


Step 3: Smooth the signal

    df["cri"] = df["cri_raw"].rolling(7).mean()

A 7-day moving average reduces noise and highlights regime shifts.


Step 4: Save the index

    df[["cri"]].to_csv(DATA_DIR / "cri.csv")

This produces the final CRI time series used by other scripts.


Interpretation
--------------

CRI > +1
Strong risk-on environment.
Altcoins gaining strength relative to BTC.

CRI between +0.5 and +1
Mild risk-on.

CRI between -0.5 and +0.5
Neutral market.

CRI between -1 and -0.5
Defensive environment.

CRI < -1
Strong defensive regime.
Capital concentrating in BTC.


Important Principle
-------------------
CRI measures **capital flow**, not price direction.

BTC price can rise while CRI falls if money concentrates in BTC.


Future Sensors (Planned)
------------------------
To stabilize the index, two additional signals will be added:

3. BTC dominance rate-of-change
4. BTC volatility compression

Final CRI = average of four normalized signals.