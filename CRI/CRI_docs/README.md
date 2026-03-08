Capital Rotation Index (CRI)
CG-hGzKESgBEPs354FJUqUYiRxG
Purpose
-------
CRI measures where capital is flowing inside the crypto market.
It does NOT predict price. It detects market regimes.

Inputs (v1)
-----------
1. ETH/BTC strength
2. SOL/BTC strength

Each signal is converted to a rolling 1-year z-score and averaged.

Interpretation
--------------

CRI > +1
Strong risk-on regime.
Capital rotating into altcoins relative to BTC.

CRI between +1 and +0.5
Mild risk-on.
Altcoins gaining relative strength.

CRI between +0.5 and -0.5
Neutral regime.
No clear leadership.

CRI between -0.5 and -1
Defensive regime.
Capital flowing back toward BTC.

CRI < -1
Strong defensive regime.
BTC dominance environment.

How to read the chart
---------------------

Black line = BTC price.

Red line = CRI (capital rotation pressure).

Green shading = risk-on regime.
Red shading = defensive regime.

Important principle
-------------------

CRI measures capital flow, not price direction.

BTC can rise while CRI falls if money concentrates into BTC.
BTC can fall while CRI rises if capital rotates into alts.

Future Improvements
-------------------

Add two additional sensors:

3. BTC dominance rate-of-change
4. BTC volatility compression

Final CRI = average of four normalized signals.