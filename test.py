import unittest
import random

from shamir import Share, Reconstruct
from operations import share_to, add_shares, mult_shares, degree_reduction


class TestShamir(unittest.TestCase):
    def generate_shares(self, pp, x, n, t):
        shares = Share(pp, x, n, t)
        print("Generated shares:")
        for s in shares:
            print(f"  Share: {s}")

        return shares

    def run_shamir(self, pp, x, n, t, label):
        print(f"\n--- {label} ---")
        print(f"Field: GF({pp}) | Secret: {x} | n: {n} | t: {t}")

        shares = self.generate_shares(pp, x, n, t)

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

    def test_share_to(self):
        """
        Test the redistribution of shares
        """

        pp = 257
        x = 200
        n = 5
        t = 2
        m = 3

        print(f"\n--- SHARE_TO TEST ---")
        print(f"Field: GF({pp}) | Secret: {x} | n: {n} | m: {m} | t: {t}")

        shares = self.generate_shares(pp, x, n, t)

        share = random.sample(shares, 1)[0]
        print(f"Using share for redistribution: {share}")
     
        subshares = share_to(pp, t, share[1], m)
        print("Generated sub-shares (with the same threshold & size = m):")
        for s in subshares:
            print(f"  Share: {s}")

        subset = random.sample(subshares, t)
        print(f"Using sub-shares for reconstruction: {subset}")

        reconstructed = Reconstruct(pp, subset)
        print(f"Reconstructed secret: {reconstructed}")
        self.assertEqual(reconstructed, share[1])
        print("Secret correctly reconstructed!")
        
    
    def test_add_shares(self):
        """
        Test addition of full (n-out-of-n) Shamir sharings.
        This simulates 〈z〉 = 〈x〉 + 〈y〉 and confirms that
        Reconstruct(〈z〉) == x + y mod p.
        """

        pp = 103 
        n = 5
        t = n
        x = 33
        y = 42
        expected = ( x + y ) % pp

        x_shares = Share(pp,x,n,n)
        y_shares = Share(pp,y,n,n)

        z_shares = add_shares(pp, x_shares, y_shares)
        recovered = Reconstruct(pp, z_shares)

        print(f"\n--- ADD_SHARES TEST ---")
        print(f"p = {pp}, n = {n}, t = {t}, expected product = {expected}")
        print(f"x = {x}, y = {y}")
        print(f"x_shares: {x_shares}")
        print(f"y_shares: {y_shares}")
        print(f"z_shares (after add): {z_shares}")
        print(f"reconstructed = {recovered}")

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

        z_shares = add_shares(pp, x_shares, y_shares)

        # Select t common indices for both subsets
        subset_indices = sorted(random.sample(range(1, n+1), t))
        z_subset = sorted([s for s in z_shares if s[0] in subset_indices], key=lambda s: s[0])

        recovered = Reconstruct(pp, z_subset) 

        print(f"\n--- ADD_SHARES WITH SUBSET ---")
        print(f"p = {pp}, n = {n}, t = {t}, expected product = {expected}")
        print(f"x = {x}, y = {y}")
        print(f"x_shares: {x_shares}")
        print(f"y_shares: {y_shares}")
        print(f"z_shares (after add): {z_shares}")
        print(f"subset_indices used for reconstruction: {subset_indices}")
        print(f"z_subset used: {z_subset}")
        print(f"reconstructed = {recovered}")

        self.assertEqual(recovered, expected)
        print("Secret correctly reconstructed!")

    def test_mult_shares_no_degree_reduction_error(self):
        """
        Test that multiplying two Shamir sharings using only t shares (with matching indices) 
        doesn't work because the degree of the polynomial has grown.
        """

        pp = 67
        n = 5
        t = 2 
        x = 3
        y = 4 
        expected = ( x * y ) % pp

        x_shares = Share(pp, x, n, t)
        y_shares = Share(pp, y, n, t)

        z_shares = mult_shares(pp, x_shares, y_shares)

        subset_indices = sorted(random.sample(range(1, n+1), t))
        z_subset = sorted([s for s in z_shares if s[0] in subset_indices], key=lambda s: s[0])

        recovered = Reconstruct(pp, z_subset)

        print(f"\n--- MULT_SHARES WITH SUBSET ERROR ---")
        print(f"p = {pp}, n = {n}, t = {t}, expected product = {expected}")
        print(f"x = {x}, y = {y}")
        print(f"x_shares: {x_shares}")
        print(f"y_shares: {y_shares}")
        print(f"z_shares (degree 2*t-1): {z_shares}")
        print(f"subset_indices used for reconstruction: {subset_indices}")
        print(f"z_subset used: {z_subset}")
        print(f"reconstructed = {recovered}")

        self.assertNotEqual(recovered, expected)
        print("Secret NOT reconstructed because the polynomial degree has grown and now it needs (2*t - 1) unique shares to reconstruct the secret!")

    def test_mult_shares_no_degree_reduction_correct(self):
        """
        Test that multiplying two Shamir sharings using (2*t-1) shares (with matching indices) 
        to reconstruct the secret gives the correct secret.
        """

        pp = 67
        n = 5
        t = 2 
        x = 3
        y = 4 
        expected = ( x * y ) % pp

        x_shares = Share(pp, x, n, t)
        y_shares = Share(pp, y, n, t)

        z_shares = mult_shares(pp, x_shares, y_shares)
        
        subset_indices = sorted(random.sample(range(1, n+1), 2*t-1))
        z_subset = sorted([s for s in z_shares if s[0] in subset_indices], key=lambda s: s[0])

        recovered = Reconstruct(pp, z_subset)

        print(f"\n--- MULT_SHARES WITH SUBSET CORRECT ---")
        print(f"p = {pp}, n = {n}, t = {t}, expected product = {expected}")
        print(f"x = {x}, y = {y}")
        print(f"x_shares: {x_shares}")
        print(f"y_shares: {y_shares}")
        print(f"z_shares (degree 2*t-1): {z_shares}")
        print(f"subset_indices used for reconstruction: {subset_indices}")
        print(f"z_subset used: {z_subset}")
        print(f"reconstructed = {recovered}")

        self.assertEqual(recovered, expected)
        print("Secret correctly reconstructed!")

    def test_mult_shares_with_degree_reduction(self):
        """
        Test that multiplying two Shamir sharings and then applying degree reduction
        allows the secret to be reconstructed using only t shares.
        """

        pp = 67
        n = 5
        t = 2 
        x = 3
        y = 4 
        expected = ( x * y ) % pp

        x_shares = Share(pp, x, n, t)
        y_shares = Share(pp, y, n, t)

        z_shares = mult_shares(pp, x_shares, y_shares)

        reduced_shares = degree_reduction(pp, z_shares, t)

        subset_indices = sorted(random.sample(range(1, n+1), t))
        reduced_subset = sorted([s for s in reduced_shares if s[0] in subset_indices], key=lambda s: s[0])

        recovered = Reconstruct(pp, reduced_subset)

        print(f"\n--- MULT_SHARES WITH DEGREE REDUCTION ---")
        print(f"p = {pp}, n = {n}, t = {t}, expected product = {expected}")
        print(f"x = {x}, y = {y}")
        print(f"x_shares: {x_shares}")
        print(f"y_shares: {y_shares}")
        print(f"z_shares (after mult): {z_shares}")
        print(f"reduced_shares (after degree reduction): {reduced_shares}")
        print(f"subset_indices used for reconstruction: {subset_indices}")
        print(f"reduced_subset used: {reduced_subset}")
        print(f"reconstructed = {recovered}")

        self.assertEqual(recovered, expected)
        print("Secret correctly reconstructed after degree reduction!")


if __name__ == "__main__":
    unittest.main()
