"""
Operations on Shares for Shamir Secret Sharing

Based on:
  Daniel Kales, "Secret Sharing", Graz University of Technology.
  https://www.isec.tugraz.at/wp-content/uploads/teaching/mfc/secret_sharing.pdf

Implements:
  - add_shares(pp, x_shares, y_shares): adds two shares modulo pp
  - mul_shares(pp, x_shares, y_shares): multiplies two shares modulo pp (without degree reduction)

Note:
  - Operations assume that shares correspond to polynomials over GF(pp)
  - Addition is linear and preserves the threshold
  - Multiplication increases the degree of the polynomial, which increase the minimum threshold (t) required to reconstruct the secret.
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

    B = vandermonde_matrix(pp, xs, n)     

    P = projection_matrix(pp, n , t)

    B_inv = B.inv_mod(pp)

    A = (B * P * B_inv) % pp

    S = Matrix(ys)
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


