"""
Operations on Shares for Shamir Secret Sharing

Based on:
  - Daniel Kales, "Secret Sharing", Graz University of Technology.
    https://www.isec.tugraz.at/wp-content/uploads/teaching/mfc/secret_sharing.pdf
  - Michael Ben-Or, Shafi Goldwasser, and Avi Wigderson,
    "Completeness Theorems for Non-Cryptographic Fault-Tolerant Distributed Computation",
    Proceedings of the 20th ACM Symposium on Theory of Computing (STOC), 1988.
    https://doi.org/10.1145/62212.62213

Implements:
  - add_shares(pp, x_shares, y_shares): adds two shares modulo pp
  - mult_shares(pp, x_shares, y_shares): multiplies two shares modulo pp (without degree reduction)
  - degree_reduction(pp, z_shares, t): reduces the degree of a Shamir sharing using BGW (including the randomization step to protect intermediate coefficients)

Note:
  - Operations assume that shares correspond to polynomials over GF(pp)
  - Addition is linear and preserves the threshold
  - Multiplication increases the degree of the polynomial, which increase the minimum threshold (t) required to reconstruct the secret.
  - BGW degree reduction is needed to restore the original threshold (t)
"""

from sympy import Matrix
import random

from shamir import Share, Reconstruct

def add_shares(pp, x_shares, y_shares):
    if len(x_shares) != len(y_shares):
        raise ValueError("Both shares must have the same number of elements")

    z_shares = []
    for (ix, yx), (iy, yy) in zip(x_shares, y_shares):
        if ix != iy:
            raise ValueError("Shares x-coordinates must match.")
        zi = ( yx + yy ) % pp
        z_shares.append((ix,zi))

    return z_shares

def mult_shares(pp, x_shares, y_shares):
    if len(x_shares) != len(y_shares):
        raise ValueError("Both shares must have the same number of elements")

    z_shares = []
    for (ix, yx), (iy, yy) in zip(x_shares, y_shares):
        if ix != iy:
            raise ValueError("Shares x-coordinates must match.")
        zi = ( yx * yy ) % pp
        z_shares.append((ix,zi))

    return z_shares

def degree_reduction(pp, z_shares, t):
    n = len(z_shares)
    xs = [ x for x, _ in z_shares]
    ys = [ y for _, y in z_shares]

    # Construct the truncation matrix 
    B = vandermonde_matrix(pp, xs, n)     
    P = projection_matrix(pp, n , t)
    B_inv = B.inv_mod(pp)
    A = (B * P * B_inv) % pp

    # Randomize in order to hide intermediate coefficients
    max_deg = 2*(t-1)
    q_coeffs = [0]
    for k in range(1, max_deg+1):
        total = sum(random.randint(0, pp - 1) for _ in range(n)) % pp
        q_coeffs.append(total)

    # Creating new randomized shares 
    randomized = []
    for xi, zi in z_shares:
        qi = 0
        for k in range(1, max_deg + 1):
            term = (q_coeffs[k] * pow(xi, k, pp)) % pp
            qi = (qi + term) % pp

        randomized.append((xi, (zi + qi) % pp))

    # Apply degree reduction
    S = Matrix([yi for _, yi in randomized])
    R = (A * S) % pp

    new_shares = list(zip(xs, [int(v) for v in R]))
    return new_shares

def vandermonde_matrix(pp, xs, n):
    return Matrix([[pow(x, j, pp) for j in range(n)] for x in xs])

def projection_matrix(pp, n, t):
    matrix = Matrix.zeros(n, n)
    for i in range(t):
        matrix[i, i] = 1
    return matrix 


