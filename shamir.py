"""
Shamir Secret Sharing Scheme 

Based on:
  - Daniel Kales, "Secret Sharing", Graz University of Technology.
    https://www.isec.tugraz.at/wp-content/uploads/teaching/mfc/secret_sharing.pdf

Implements:
  - Share(pp, x, n, t): splits a secret x into n shares with reconstruction threshold t
  - Reconstruct(pp, shares): reconstructs the original secret using Lagrange interpolation

Note:
  - The implementation follows the description in Scheme 3 of the reference
  - All arithmetic is performed in the finite field GF(pp), where pp is a user-defined prime.
"""

import random

# Gen() is not implemented because the field prime 'pp' must be defined by the user in advance.
  
def Share(pp, x, n, t):
    if n < t:
        raise ValueError("The number of shares 'n' has to be higher or equal to the treshold 't'.")
    if not (0 <= x < pp):
        raise ValueError("The secret 'x' has to be an element of the finite field 'F_pp'.")
    if pp <= n: 
        raise ValueError("The size of the finite field 'F_pp' must be greater than the number of shares 'n'.")

    coeffs = [x] + [random.randint(1, pp - 1) for _ in range(1, t)]

    shares = []
    for i in range(1, n+1):
        xi = 0 
        for power, coeff in enumerate(coeffs):
            term = (coeff * pow(i, power, pp)) % pp
            xi = (xi + term) % pp

        shares.append((i, xi))

    return shares

def Reconstruct(pp, t_shares):
    for _, yi in t_shares:
        if not (0 <= yi < pp): 
            raise ValueError(f"The share 'y_i'={yi} has to be an element of the finite field 'F_pp'.")

    return lagrange_interpolation(pp, t_shares)
        
def lagrange_interpolation(pp, t_shares):
    secret = 0

    for i in range(len(t_shares)):
        xi, yi = t_shares[i]

        num = 1
        denom = 1
        for j in range(len(t_shares)):
            if i == j:
                continue
            xj, _ = t_shares[j]
            num = (num * (-xj)) % pp
            denom = (denom * (xi - xj)) % pp

        denom_inv = pow(denom, -1, pp)
        li = (num * denom_inv) % pp

        secret = (secret + yi * li) % pp

    return secret


