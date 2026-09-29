import unittest
from src.black_scholes import black_scholes

class TestBlackScholes(unittest.TestCase):
    def test_put_call_parity(self):
        S, K, T, r, sigma, q = 100, 105, 30/365, 0.04, 0.30, 0.0
        c = black_scholes(S, K, T, r, sigma, "call", q)
        p = black_scholes(S, K, T, r, sigma, "put", q)
        lhs = c.price - p.price
        rhs = S - K * __import__("math").exp(-r*T)
        self.assertAlmostEqual(lhs, rhs, places=9)

    def test_call_delta_bounds(self):
        x = black_scholes(100, 100, 1, 0.05, 0.20, "call")
        self.assertGreater(x.delta, 0)
        self.assertLess(x.delta, 1)

    def test_put_delta_bounds(self):
        x = black_scholes(100, 100, 1, 0.05, 0.20, "put")
        self.assertGreater(x.delta, -1)
        self.assertLess(x.delta, 0)

if __name__ == "__main__":
    unittest.main()
