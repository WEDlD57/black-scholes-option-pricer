import argparse
from src.black_scholes import black_scholes

def main():
    p = argparse.ArgumentParser(description="Black-Scholes European option pricer + Greeks")
    p.add_argument("--type", choices=["call", "put"], required=True)
    p.add_argument("--spot", type=float, required=True)
    p.add_argument("--strike", type=float, required=True)
    p.add_argument("--days", type=float, required=True)
    p.add_argument("--rate", type=float, required=True, help="Percent, e.g. 4.5")
    p.add_argument("--vol", type=float, required=True, help="Percent, e.g. 30")
    p.add_argument("--dividend", type=float, default=0.0, help="Percent")
    a = p.parse_args()

    result = black_scholes(
        a.spot, a.strike, a.days / 365.0,
        a.rate / 100.0, a.vol / 100.0,
        a.type, a.dividend / 100.0
    )

    print(f"\n{a.type.upper()} — BLACK-SCHOLES-MERTON")
    print("-" * 38)
    print(f"Theoretical price : ${result.price:.4f}")
    print(f"Delta             : {result.delta:.6f}")
    print(f"Gamma             : {result.gamma:.6f}")
    print(f"Theta / day       : {result.theta_per_day:.6f}")
    print(f"Vega / 1% IV      : {result.vega_per_1pct:.6f}")
    print(f"Rho / 1% rate     : {result.rho_per_1pct:.6f}")
    print(f"d1                : {result.d1:.6f}")
    print(f"d2                : {result.d2:.6f}")

if __name__ == "__main__":
    main()
