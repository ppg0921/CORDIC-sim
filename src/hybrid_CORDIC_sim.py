import numpy as np
import matplotlib.pyplot as plt

def cordic_step_n2(x, y, res_angle):
    """Computes one CORDIC step for n=2 with correct scaling factor."""
    print(f"Initial angle={res_angle}")
    angle_n2 = np.arctan(2 ** -2)
      # Correct scaling factor
    if np.abs(res_angle) >= 10.5775 and np.abs(res_angle) < 22.5:
        d = 1 if res_angle > 0 else -1
    else:
        d = 0
    # d = 1 if res_angle >= np.rad2deg(2**(-2)) else -1
    K_n2 = 1 / np.sqrt(1 + 2**-4) if d!=0 else 1
    x_new = (x - d * y * (2 ** -2))
    y_new = (y + d * x * (2 ** -2))
    res_angle -= d * np.rad2deg(angle_n2)
    print(f"n=2, d={d}, angle={res_angle}")
    return x_new, y_new, res_angle, K_n2

def cordic_step_n3(x, y, res_angle):
    """Computes one CORDIC step for n=3 with correct scaling factor."""
    angle_n3 = np.arctan(2 ** -3)
    
    if np.abs(res_angle) >= 5.3505 and np.abs(res_angle) < 10.5775:
        d = 1 if res_angle > 0 else -1
    else:
        d = 0
    # d = 1 if res_angle >= np.rad2deg(2**(-3)) else -1
    K_n3 = 1 / np.sqrt(1 + 2**-6) if d!=0 else 1 # Correct scaling factor
    x_new = (x - d * y * (2 ** -3))
    y_new = (y + d * x * (2 ** -3))
    res_angle -= d * np.rad2deg(angle_n3)
    print(f"n=3, d={d}, angle={res_angle}")
    return x_new, y_new, res_angle, K_n3

def cordic_step_n4(x, y, res_angle, n):
    if np.deg2rad(np.abs(res_angle)) >= (np.arctan(2**(-n))+np.arctan(2**(-n-1)))/2.0 and np.deg2rad(np.abs(res_angle)) < (np.arctan(2**(-n))+np.arctan(2**(-n+1)))/2.0:
        d = 1 if res_angle > 0 else -1
    else:
        d = 0
    x_new = (1-2**(-2*n+1))*x - d*(2**(-n))*y
    y_new = d*(2**(-n))*x + (1-2**(-2*n+1))*y
    res_angle -= d*np.rad2deg(np.arctan(2**(-n)))
    print(f"n={n}, d={d}, angle={res_angle}, rotated angle={(np.rad2deg(np.arctan(2**(-n))))}")
    return x_new, y_new, res_angle
    

def cordic_rotation(x, y, theta, iterations, mode="traditional"):
    """
    Simulates the CORDIC algorithm in rotation mode.
    - `x, y` : Initial vector components.
    - `theta` : Target rotation angle in radians.
    - `iterations` : Number of iterations.
    - `mode` : "traditional" for standard CORDIC, "hybrid" for optimized version.
    """
    # K = np.prod([1 / np.sqrt(1 + 2**(-2*i)) for i in range(2, 4)])  # Compute full scaling factor
    # print("K=", K) 
    K = 1
    for i in range(2, iterations):
        if i == 2:
            x, y, theta, Ki = cordic_step_n2(x, y, theta)
            K *= Ki
            continue
        elif i == 3:
            x, y, theta, Ki = cordic_step_n3(x, y, theta)
            K *= Ki
            continue
        
        angle_i = np.arctan(2 ** -i)
        di = 1 if theta >= 0 else -1
        
        if mode == "hybrid" and i >= 4:  # First-order approximation for large i
            x_new, y_new, theta = cordic_step_n4(x, y, theta, i)
        else:
            x_new = x - di * y * (2 ** -i)
            y_new = y + di * x * (2 ** -i)
            theta -= di * angle_i
        
        
        x, y = x_new, y_new
    
    return x * K, y * K

test_angles = np.linspace(-22.49, 22.49, 50)
x_init, y_init = 1, 0  # Unit vector
iterations = 8

results_hybrid = [cordic_rotation(x_init, y_init, theta, iterations, "hybrid") for theta in test_angles]
results_hybrid = np.array(results_hybrid)
true_cos_values = np.cos(np.deg2rad(test_angles))
error_hybrid = np.abs(results_hybrid[:, 0] - true_cos_values)


# Plot results in subplots
fig, axs = plt.subplots(2, 1, figsize=(8, 10))

# First subplot: Hybrid CORDIC vs True cos(θ)
axs[0].plot(test_angles, true_cos_values, 'k--', label='True cos(θ)')
axs[0].plot(test_angles, results_hybrid[:, 0], 'b-', label='Hybrid CORDIC')
axs[0].set_xlabel('Angle (degrees)')
axs[0].set_ylabel('cos(θ)')
axs[0].legend()
axs[0].set_title('Hybrid vs. True cos(θ)')
axs[0].grid()

# Second subplot: Error rate
axs[1].plot(test_angles, error_hybrid, 'r-', label='Error (Hybrid CORDIC)')
axs[1].set_xlabel('Angle (degrees)')
axs[1].set_ylabel('Absolute Error')
axs[1].set_title('Error Rate of Hybrid CORDIC vs. Angle')
axs[1].legend()
axs[1].grid()

plt.tight_layout()
plt.show()