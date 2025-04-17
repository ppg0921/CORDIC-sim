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
import utils


def cordic_division(x_init, y_init, num_iters, total_bits=16, frac_bits=13, approximate=False):
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
      if not approximate:
        # y = y + d * x * e
        # z = z - d * e
        dx = utils.quantize_to_fixed_point(d*x)
        dei = utils.quantize_to_fixed_point(-d*e)
      else:
        if d == -1:
          dx = utils.fixed_point_negation(x, total_bits=total_bits, frac_bits=frac_bits)[0]
          dei = e
        else:
          dx = utils.quantize_to_fixed_point(x, total_bits=total_bits, frac_bits=frac_bits)
          dei = -e
      shifted_x = utils.fixed_point_signed_right_shift(x=dx, shift=i, total_bits=total_bits, frac_bits=frac_bits)[0]
      y = utils.fixed_point_add(y, shifted_x, total_bits=total_bits, frac_bits=frac_bits)[0]
      z = utils.fixed_point_add(z, dei, total_bits=total_bits, frac_bits=frac_bits)[0]
    return z


def main():
    # Hardcoded input values
    x_init = 1.5       # initial x value (non-zero)
    y_init = 1       # initial y value
    num_iters = 16     # number of CORDIC iterations (≤53)
    total_bits = 16
    frac_bits = 11
    compared_to_no_approx = True
    
    ideal = y_init / x_init
    if compared_to_no_approx:
      # Compare with non-approximate version
      ideal = cordic_division(x_init=x_init, y_init=y_init, num_iters=num_iters, approximate=False, total_bits=total_bits, frac_bits=frac_bits)

    z_approx = cordic_division(x_init=x_init, y_init=y_init, num_iters=num_iters, approximate=True, total_bits=total_bits, frac_bits=frac_bits)
    rel_error = (z_approx - ideal) / ideal * 100

    print(f"Approximate y/x    = {z_approx}")
    print(f"Ideal y/x          = {ideal}")
    print(f"Relative error     = {rel_error:.4f}%")


if __name__ == '__main__':
    main()
