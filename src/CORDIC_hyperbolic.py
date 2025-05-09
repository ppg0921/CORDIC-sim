import math
import numpy as np
import matplotlib.pyplot as plt

def cordic_hyperbolic_rotation(z_input, iterations=20):
    # Initial values
    x = 1.207497068
    y = 0.0
    z = z_input

    # Precompute arctanh values and K'
    atanhs = []
    K = 1.0
    i = 1  # Start from i = 1 to avoid math domain error
    count = 0
    repeat_set = {4, 13}

    while count < iterations:
        e_i = math.atanh(2 ** -i)
        if i in repeat_set:
            atanhs.append((i, e_i))
            atanhs.append((i, e_i))  # repeat once
            K *= (1 - 2 ** (-2 * i)) ** -1.5
            count += 2
        else:
            atanhs.append((i, e_i))
            K *= (1 - 2 ** (-2 * i)) ** -0.5
            count += 1
        i += 1

    # K_inv = 1 / K
    # x *= K_inv
    # y *= K_inv

    # Run CORDIC iterations
    for i, e_i in atanhs:
        d = 1 if z >= 0 else -1
        pow2_i = 2 ** -i
        x_new = x + d * y * pow2_i
        y_new = y + d * x * pow2_i
        z -= d * e_i
        x, y = x_new, y_new

    return x, y


z_vals = np.linspace(0, 1.0, 100)
relative_errors = []

for z in z_vals:
    x_final, y_final = cordic_hyperbolic_rotation(z, iterations=8)
    cordic_output = x_final + y_final
    expected = math.exp(z)
    rel_error = abs(cordic_output - expected) / expected * 100
    relative_errors.append(rel_error)

# Plot the graph
plt.figure(figsize=(8, 5))
plt.plot(z_vals, relative_errors, label='Relative Error (%)')
plt.xlabel('Input z')
plt.ylabel('Relative Error (%)')
plt.title('CORDIC Hyperbolic Rotation Mode: Relative Error vs z')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("../result/cordic_hyperbolic_rotation.png", dpi=300)  # You can change filename or dpi as needed
plt.show()
# Input value
# z_val = 0.9
# x_final, y_final = cordic_hyperbolic_rotation(z_val)

# # Compute expected and error
# cordic_output = x_final + y_final
# expected = math.exp(z_val)
# error = abs(cordic_output - expected)/expected * 100 

# # Print results
# print(f"x_final = {x_final}")
# print(f"y_final = {y_final}")
# print(f"x + y    = {cordic_output}")
# print(f"e^{z_val} = {expected}")
# print(f"Absolute Error = {error:.4f}%")
