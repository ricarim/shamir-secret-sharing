import random


def Gen():
    pp = 17
    return pp


def Share(pp, x, n, t):
    if n < t:
        raise ValueError("The number of shares 'n' has to be higher or equal to the treshold 't'.")
    if not (0 <= x <= pp-1):
        raise ValueError("The secret 'x' has to be an element of the finite field 'F_pp'.")
    if pp <= n: 
        raise ValueError("The size of the field 'F_pp' must be greater than the number of shares 'n'.")

    coeffs = [x]

    for i in range(1, t):
        coeffs.append(random.randint(0, pp-1))

    shares = []
    for i in range(1, n+1):
        xi = 0 
        for power, coeff in enumerate(coeffs):
            term = (coeff * pow(i, power, pp)) % pp
            xi = (xi + term) % pp

        shares.append((i, xi))

    return shares



def Reconstruct(pp, t_shares):
    for i in range(len(t_shares)):
        xi, yi = t_shares[i]
        if not (0 <= yi <= pp-1): 
            raise ValueError(f"The share 'y_i'={yi} has to be an element of the finite field 'F_pp'.")

    return lagrange_interpolation(pp, t_shares)
        
        

def lagrange_interpolation(pp, t_shares):
    secret = 0

    for i in range(len(t_shares)):
        xi, yi = t_shares[i]

        numerator = 1
        denominator = 1
        for j in range(len(t_shares)):
            if j == i:
                continue
            xj, _ = t_shares[j]
            numerator = (numerator * (-xj)) % pp
            denominator = (denominator * (xi - xj)) % pp

        inv_denominator = pow(denominator, -1, pp)
        lagrange_coeff = (numerator * inv_denominator) % pp

        term = (yi * lagrange_coeff) % pp
        secret = (secret + term) % pp

    return secret




pp = gen()
shares = share(pp, 11 , 5, 3)
for s in shares:
    print(s)


subset = random.sample(shares, 3)
reconstruct = reconstruct(pp, subset)
print(reconstruct)



