import math
from dataclasses import dataclass

SQRT_2PI = math.sqrt(2.0 * math.pi)

def norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / SQRT_2PI

def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

@dataclass(frozen=True)
class OptionResult:
    price: float
    delta: float
    gamma: float
    theta_per_day: float
    vega_per_1pct: float
    rho_per_1pct: float
    d1: float
    d2: float

def black_scholes(S: float, K: float, T: float, r: float, sigma: float,
                  option_type: str = "call", q: float = 0.0) -> OptionResult:
    """European Black-Scholes-Merton price and Greeks.

    Rates/volatility are decimals (e.g. 5% -> 0.05).
    T is years. Theta is reported per calendar day.
    Vega/Rho are reported per 1 percentage-point change.
    """
    if S <= 0 or K <= 0:
        raise ValueError("S and K must be positive.")
    if T <= 0:
        raise ValueError("T must be positive.")
    if sigma <= 0:
        raise ValueError("sigma must be positive.")

    kind = option_type.strip().lower()
    if kind not in {"call", "put"}:
        raise ValueError("option_type must be 'call' or 'put'.")

    sqrt_t = math.sqrt(T)
    disc_r = math.exp(-r * T)
    disc_q = math.exp(-q * T)

    d1 = (math.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * sqrt_t)
    d2 = d1 - sigma * sqrt_t
    pdf = norm_pdf(d1)

    gamma = disc_q * pdf / (S * sigma * sqrt_t)
    vega = S * disc_q * pdf * sqrt_t / 100.0

    if kind == "call":
        price = S * disc_q * norm_cdf(d1) - K * disc_r * norm_cdf(d2)
        delta = disc_q * norm_cdf(d1)
        theta_year = (
            -(S * disc_q * pdf * sigma) / (2 * sqrt_t)
            - r * K * disc_r * norm_cdf(d2)
            + q * S * disc_q * norm_cdf(d1)
        )
        rho = K * T * disc_r * norm_cdf(d2) / 100.0
    else:
        price = K * disc_r * norm_cdf(-d2) - S * disc_q * norm_cdf(-d1)
        delta = disc_q * (norm_cdf(d1) - 1.0)
        theta_year = (
            -(S * disc_q * pdf * sigma) / (2 * sqrt_t)
            + r * K * disc_r * norm_cdf(-d2)
            - q * S * disc_q * norm_cdf(-d1)
        )
        rho = -K * T * disc_r * norm_cdf(-d2) / 100.0

    return OptionResult(
        price=price, delta=delta, gamma=gamma,
        theta_per_day=theta_year / 365.0,
        vega_per_1pct=vega, rho_per_1pct=rho, d1=d1, d2=d2
    )
