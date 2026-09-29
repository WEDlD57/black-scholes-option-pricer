# Black-Scholes Option Pricer

A dependency-free Python implementation of the Black-Scholes-Merton model for European call and put options.

## Features
- European call and put pricing
- Continuous dividend yield
- Delta, Gamma, Theta, Vega, and Rho
- d1 and d2 output
- Input validation
- Put-call parity and Greek sanity tests
- Command-line interface

## Conventions
- Interest rates, dividend yield, and volatility are entered as percentages in the CLI.
- Theta is reported per calendar day.
- Vega is the price change for a 1 percentage-point change in volatility.
- Rho is the price change for a 1 percentage-point change in the risk-free rate.

## Example

```bash
python3 app.py --type call --spot 100 --strike 105 --days 30 --rate 4 --vol 30
```

Put:

```bash
python3 app.py --type put --spot 100 --strike 105 --days 30 --rate 4 --vol 30
```

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## Model limitations
Black-Scholes-Merton assumes lognormal underlying-price dynamics, constant volatility and rates, frictionless markets, and European exercise. Real option market prices can differ materially, especially because implied volatility varies by strike and expiry and American-style contracts can permit early exercise.

## Project structure

```text
.
├── app.py
├── src/
│   └── black_scholes.py
├── tests/
│   └── test_pricer.py
└── README.md
```
