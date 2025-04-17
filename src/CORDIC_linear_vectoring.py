#!/usr/bin/env python3
"""
Simulate CORDIC linear vectoring mode for performing division y/x.

Iterations:
    x_{i+1} = x_i
    y_{i+1} = y_i + d_i * x_i * 2^{-i}
    z_{i+1} = z_i - d_i * 2^{-i}

where:
    d_i = 1  if x_i * y_i < 0
        = -1 otherwise

At the end, z approximates y_init/x_init.  This script prints the approximate quotient, the ideal quotient, and the relative error.

Input limits:
  - x_init must be non-zero (division by zero not allowed).
  - x_init and y_init should be within the range of Python floats (~±1e308).
  - For maximum precision, set num_iters ≤ 53 (double-precision mantissa bits).
"""

def cordic_division(x_init, y_init, num_iters):
    """
    Perform CORDIC linear vectoring algorithm to compute y_init/x_init.

    Args:
        x_init (float): non-zero initial x value.
        y_init (float): initial y value.
        num_iters (int): number of iterations (≤ 53 for full precision).

    Returns:
        float: approximation of y_init/x_init.
    """
    # Validate inputs
    if x_init == 0.0:
        raise ValueError("x_init must be non-zero for division.")
    if num_iters < 1:
        raise ValueError("num_iters must be at least 1.")

    x = float(x_init)
    y = float(y_init)
    z = 0.0

    # Perform iterations
    for i in range(num_iters):
        e = 2.0 ** (-i)
        d = 1 if x * y < 0 else -1
        # Vectoring updates
        y = y + d * x * e
        z = z - d * e

    return z


def main():
    # Hardcoded input values
    x_init = 3.0       # initial x value (non-zero)
    y_init = 1.5       # initial y value
    num_iters = 20     # number of CORDIC iterations (≤53)

    z_approx = cordic_division(x_init, y_init, num_iters)
    ideal = y_init / x_init
    rel_error = (z_approx - ideal) / ideal

    print(f"Approximate y/x    = {z_approx}")
    print(f"Ideal y/x          = {ideal}")
    print(f"Relative error     = {rel_error}")


if __name__ == '__main__':
    main()
