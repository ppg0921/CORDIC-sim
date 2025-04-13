def fixed_point_negation(x, total_bits=16, frac_bits=13, output_bits=None, output_frac_bits=None):
    # Step 1: Compute scale
    if output_bits is None or output_frac_bits is None:
        output_bits = total_bits
        output_frac_bits = frac_bits
    scale = 1 << frac_bits

    # Step 2: Convert float to fixed-point signed integer
    fixed = int(round(x * scale))

    # Step 3: Ensure value fits in two's complement
    max_val = (1 << (total_bits - 1)) - 1
    min_val = -1 << (total_bits - 1)
    if fixed > max_val or fixed < min_val:
        raise ValueError(f"Value {x} out of range for {total_bits}-bit fixed-point")

    # Step 4: Convert to unsigned total_bits-bit two's complement
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

    # Step 8: Quantize to output format
    out_scale = 1 << output_frac_bits
    quantized_int = int(round(result * out_scale))

    # Clip to representable range
    output_int_bits = output_bits - 1 - output_frac_bits
    out_min = -1 << output_int_bits
    out_max = (1 << output_int_bits) - 1
    quantized_int = max(out_min * out_scale, min(out_max * out_scale, quantized_int))

    # Final quantized float and binary
    quantized_float = quantized_int / out_scale
    quantized_binary = format(quantized_int & ((1 << output_bits) - 1), f'0{output_bits}b')

    return quantized_float, (format(fixed_unsigned, f'0{total_bits}b'), format(negated, f'0{total_bits}b')), quantized_binary


def fixed_point_add(x, y, total_bits=16, frac_bits=13, output_bits=None, output_frac_bits=None):
    if output_bits is None or output_frac_bits is None:
        output_bits = total_bits
        output_frac_bits = frac_bits
    scale = 1 << frac_bits
    max_val = (1 << (total_bits - 1)) - 1
    min_val = -1 << (total_bits - 1)

    # Convert to fixed-point representation
    x_fixed = int(round(x * scale))
    y_fixed = int(round(y * scale))

    # Perform fixed-point addition
    result_fixed = x_fixed + y_fixed

    # Saturate to fixed-point input range
    result_fixed = max(min_val, min(max_val, result_fixed))

    # Convert back to float
    result_float = result_fixed / scale

    # Quantize result to output format
    out_scale = 1 << output_frac_bits
    quantized_int = int(round(result_float * out_scale))

    # Saturate to output range
    output_int_bits = output_bits - 1 - output_frac_bits
    out_min = -1 << output_int_bits
    out_max = (1 << output_int_bits) - 1
    quantized_int = max(out_min * out_scale, min(out_max * out_scale, quantized_int))

    # Final quantized float and binary representation
    quantized_float = quantized_int / out_scale
    quantized_binary = format(quantized_int & ((1 << output_bits) - 1), f'0{output_bits}b')

    return quantized_float, quantized_int, quantized_binary


def fixed_point_signed_right_shift(x, shift, total_bits=16, frac_bits=13, output_bits=None, output_frac_bits=None):
    if output_bits is None or output_frac_bits is None:
        output_bits = total_bits
        output_frac_bits = frac_bits
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

def quantize_to_fixed_point(x, total_bits=16, frac_bits=13):
    int_bits = total_bits - 1 - frac_bits  # 1 sign bit

    # Calculate scaling factor
    scale = 1 << frac_bits

    # Fixed-point value (rounded)
    fixed_val = int(round(x * scale))

    # Get representable range
    min_val = - (1 << (int_bits))
    max_val = (1 << (int_bits)) - (1 / scale)

    # Clip to range (in float)
    x_clipped = max(min(x, max_val), min_val)

    # Re-quantize after clipping
    quantized = round(x_clipped * scale) / scale

    return quantized




def test_negation(total_bits=16, frac_bits=13):
  x = 1.6746  # Represented as 00011010 (approx.)
  neg_val, orig_bin, neg_bin = fixed_point_negation(x, total_bits=total_bits, frac_bits=frac_bits)

  print(f"Original x: {x}")
  print(f"Fixed-point binary: {orig_bin}")
  print(f"Negated binary:     {neg_bin}")
  print(f"Bitwise negation result (float): {neg_val}")

def test_addition(total_bits=16, frac_bits=13, output_bits=16, output_frac_bits=13):
  x = 1.00387
  y = -0.38763
  true_result = x + y
  result_float, result_fixed, result_binary = fixed_point_add(x, y, total_bits=total_bits, frac_bits=frac_bits)
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
  
def test_quantization():
  x = -1.6184
  quantized = quantize_to_fixed_point(x, total_bits=8, frac_bits=5)
  print(f"Original x: {x}")
  print(f"Quantized to 8-bit fixed point (5 fractional bits): {quantized}")

if __name__ == "__main__":
  test_addition(total_bits=16, frac_bits=13)
  # test_shift()
  # test_quantization()
  