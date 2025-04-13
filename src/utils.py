def fixed_point_negation(x, total_bits=16, int_bits=2, frac_bits=13):
  # Step 1: Compute scale
  scale = 1 << frac_bits  # = 2^frac_bits

  # Step 2: Convert float to fixed-point signed integer
  fixed = int(round(x * scale))

  # Step 3: Ensure value fits in two's complement
  max_val = (1 << (total_bits - 1)) - 1
  min_val = -1 << (total_bits - 1)
  if fixed > max_val or fixed < min_val:
      raise ValueError(f"Value {x} out of range for {total_bits}-bit fixed-point")

  # Step 4: Convert to unsigned 8-bit representation (two's complement)
  mask = (1 << total_bits) - 1
  fixed_unsigned = fixed & mask

  # Step 5: Bitwise negation
  negated = ~fixed_unsigned & mask

  # Step 6: Convert back to signed integer
  if negated & (1 << (total_bits - 1)):
      signed = negated - (1 << total_bits)
  else:
      signed = negated

  # Step 7: Convert back to float
  result = signed / scale
  return result, (format(fixed_unsigned, '08b'), format(negated, '08b'))

def fixed_point_add(x, y, total_bits=16, int_bits=2, frac_bits=13):
    scale = 1 << frac_bits  # Scaling factor: 2^frac_bits
    max_val = (1 << (total_bits - 1)) - 1
    min_val = -1 << (total_bits - 1)

    # Convert to fixed-point representation
    x_fixed = int(round(x * scale))
    y_fixed = int(round(y * scale))

    # Perform fixed-point addition
    result_fixed = x_fixed + y_fixed

    # Saturate if out of range
    result_fixed = max(min_val, min(max_val, result_fixed))

    # Convert back to float
    result_float = result_fixed / scale

    # Format binary output
    result_binary = format(result_fixed & ((1 << total_bits) - 1), f'0{total_bits}b')

    return result_float, result_fixed, result_binary

def fixed_point_signed_right_shift(x, shift, total_bits=16, frac_bits=13, output_bits=16, output_frac_bits=13):
    scale = 1 << frac_bits
    out_scale = 1 << output_frac_bits

    max_val = (1 << (total_bits - 1)) - 1
    min_val = -1 << (total_bits - 1)

    # Step 1: Convert float input to fixed-point int
    fixed = int(round(x * scale))
    if fixed > max_val or fixed < min_val:
        raise ValueError(f"x = {x} out of range for {total_bits}-bit input")

    # Step 2: Interpret as signed and do arithmetic right shift
    if fixed < 0:
        fixed += 1 << total_bits
        fixed = fixed - (1 << total_bits)
    shifted = fixed >> shift

    # Step 3: Convert back to float
    float_result = shifted / scale

    # Step 4: Re-quantize to n-bit output fixed-point (rounding to nearest)
    quantized = int(round(float_result * out_scale))

    # Clip to output bit range
    out_max = (1 << (output_bits - 1)) - 1
    out_min = -1 << (output_bits - 1)
    quantized = max(out_min, min(out_max, quantized))

    final_float = quantized / out_scale
    final_binary = format(quantized & ((1 << output_bits) - 1), f'0{output_bits}b')

    return final_float, quantized, final_binary





def test_negation(total_bits=16, int_bits=2, frac_bits=13):
  x = 1.625  # Represented as 00011010 (approx.)
  neg_val, orig_bin, neg_bin = fixed_point_negation(x, total_bits=total_bits, int_bits=int_bits, frac_bits=frac_bits)

  print(f"Original x: {x}")
  print(f"Fixed-point binary: {orig_bin}")
  print(f"Negated binary:     {neg_bin}")
  print(f"Bitwise negation result (float): {neg_val}")

def test_addition(total_bits=16, int_bits=2, frac_bits=13):
  x = 1.00387
  y = -0.08763
  true_result = x + y
  result_float, result_fixed, result_binary = fixed_point_add(x, y, total_bits=total_bits, int_bits=int_bits, frac_bits=frac_bits)
  relative_error = abs((result_float - true_result) / true_result) * 100
  print(f"Original x: {x}")
  print(f"Original y: {y}")
  print(f"Original result (float): {true_result}")
  print(f"Fixed-point result (float): {result_float}")
  print(f"relative error: {relative_error:.6f}%")
  
def test_shift():
  x = -1.60023
  shift_value = 2
  total_bits = 8
  frac_bits = 5
  output_bits = total_bits
  output_frac_bits = frac_bits
  result, raw, binary = fixed_point_signed_right_shift(
      x, shift=shift_value, total_bits=total_bits, frac_bits=frac_bits, output_bits=output_bits, output_frac_bits=output_frac_bits
  )

  ideal_result = x / (2 ** shift_value)
  relative_error = abs((result - ideal_result) / ideal_result) * 100
  print(f"Input float: {x}")
  print(f"Shifted + quantized float: {result}")
  print(f"ideal result (float): {ideal_result}")
  print(f"relative error: {relative_error:.04}%")
  # print(f"Quantized raw int: {raw}")
  # print(f"Binary (8-bit): {binary}")
  


if __name__ == "__main__":
  # test_addition(total_bits=8, int_bits=2, frac_bits=5)
  test_shift()
  