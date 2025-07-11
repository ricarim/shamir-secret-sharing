# Shamir Secret Sharing 

Simple Python implementation of Shamir's Secret Sharing scheme, extended with the BGW protocol for secure multiplication via **randomization** and **degree reduction**.

## Overview

- **Secret Sharing**  
  Split a secret \(s\) into \(n\) shares so that any \(t\) shares reconstruct \(s\), while fewer than \(t\) reveal nothing.
- **Linear Operations**  
  - **Addition**: add corresponding shares to obtain a sharing of \(x+y\).  
  - **Multiplication**: naively multiplies shares but raises the polynomial degree to \(2(t-1)\), requiring \(2t-1\) shares to reconstruct.
- **BGW Secure Multiplication**  
  1. **Randomization**: mask the high-degree product polynomial with a zero-constant random polynomial of degree ≤ \(2(t-1)\).  
  2. **Degree Reduction**: apply the conjugated Vandermonde projection  
     \(
       A = B\,P\,B^{-1}
     \)
     to truncate the degree back to \(t-1\), restoring the original threshold \(t\).


## Files

- `shamir.py` - contains the implementation
- `test.py` - unit tests with different field sizes and operations
- `operations.py` - provides addition and multiplication of shares

## Dependencies

- **Python3**
- **Sympy** (for matrix operations)

## References
1. Daniel Kales (Graz University): Secret Sharing
https://www.isec.tugraz.at/wp-content/uploads/teaching/mfc/secret_sharing.pdf

2. Ben-Or, Goldwasser & Wigderson (STOC’88): Completeness Theorems for Non-Cryptographic Fault-Tolerant Distributed Computation
https://doi.org/10.1145/62212.62213

