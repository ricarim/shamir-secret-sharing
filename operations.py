import numpy as np
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

