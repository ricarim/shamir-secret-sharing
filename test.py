import unittest
import random

from shamir import Share, Reconstruct


class TestShamir(unittest.TestCase):

    def run_shamir(self, pp, x, n, t, label):
        print(f"\n--- {label} ---")
        print(f"Field: GF({pp}) | Secret: {x} | n: {n} | t: {t}")

        shares = Share(pp, x, n, t)
        print("Generated shares:")
        for s in shares:
            print(f"  Share: {s}")

        subset = random.sample(shares, t)
        print(f"Using subset: {subset}")

        reconstructed = Reconstruct(pp, subset)
        print(f"Reconstructed secret: {reconstructed}")
        self.assertEqual(reconstructed, x)
        print(f"Secret correctly reconstructed!")

    def test_small_field(self):
        self.run_shamir(pp=17, x=5, n=6, t=3, label="SMALL FIELD")

    def test_medium_field(self):
        self.run_shamir(pp=257, x=200, n=10, t=4, label="MEDIUM FIELD")

    def test_large_field(self):
        self.run_shamir(pp=7919, x=4321, n=10, t=5, label="LARGE FIELD")

    def test_very_large_field(self):
        self.run_shamir(pp=104729, x=99999, n=15, t=7, label="VERY LARGE FIELD")

    def test_max_secret(self):
        self.run_shamir(pp=257, x=256, n=7, t=3, label="SECRET = p - 1")


if __name__ == "__main__":
    unittest.main()
