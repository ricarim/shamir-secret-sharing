import unittest
import random

from shamir import Share, Reconstruct
from operations import add_shares


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
        print("Secret correctly reconstructed!")

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
    
    def test_add_shares(self):
        """
        Test addition of full (n-out-of-n) Shamir sharings.
        This simulates 〈z〉 = 〈x〉 + 〈y〉 and confirms that
        Reconstruct(〈z〉) == x + y mod p.
        """

        pp = 103 
        n = 5
        x = 33
        y = 42
        expected = ( x + y ) % pp

        x_shares = Share(pp,x,n,n)
        y_shares = Share(pp,y,n,n)

        z_shares = add_shares(pp, x_shares, y_shares)
        recovered = Reconstruct(pp, z_shares)

        print(f"\n--- ADDITION OF SHARES TEST ---")
        print(f"x = {x}, y = {y}, expected x + y = {expected}, reconstructed = {recovered}")
        self.assertEqual(recovered, expected)
        print("Secret correctly reconstructed!")

    def test_add_shares_subset(self):
        """
        Test that adding two Shamir sharings using only t shares (with matching indices)
        correctly reconstructs the sum x + y mod pp.
        """

        pp = 103
        n = 5
        x = 33 
        y = 42 
        t = 3 
        expected = ( x + y ) % pp

        x_shares = Share(pp, x, n, t)
        y_shares = Share(pp, y, n, t)

        # Select t common indices for both subsets
        subset_indices = sorted(random.sample(range(1, n+1), t))
        x_subset = sorted([s for s in x_shares if s[0] in subset_indices], key=lambda s: s[0])
        y_subset = sorted([s for s in y_shares if s[0] in subset_indices], key=lambda s: s[0])

        z_shares = add_shares(pp, x_subset, y_subset)
        recovered = Reconstruct(pp, z_shares) 
        print(f"\n--- ADD_SHARES WITH SUBSET (t={t}) ---")
        print(f"x = {x}, y = {y}, expected x + y = {expected}, reconstructed = {recovered}")
        self.assertEqual(recovered, expected)
        print("Secret correctly reconstructed!")



if __name__ == "__main__":
    unittest.main()
