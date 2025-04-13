import math
import matplotlib.pyplot as plt

# CORDIC class from user's file

class CORDIC:
    def __init__(self, iterations=16):
        self.iterations = iterations
        self.K = self.compute_gain()
        self.angle_table = [math.degrees(math.atan(2 ** -i)) for i in range(self.iterations)]

    def compute_gain(self):
        gain = 1.0
        for i in range(self.iterations):
            gain *= 1 / math.sqrt(1 + 2 ** (-2 * i))
        return gain

    def rotate(self, x, y, angle_deg, mode="circular", offset=5):
        """
        Rotation mode (in degrees)
        mode = 'circular' or 'linear'
        """
        z = angle_deg
        x_new, y_new = x, y

        for i in range(self.iterations):
            d = 1 if z >= 0 else -1

            if mode == "circular":
                x_temp = x_new - d * y_new * (2 ** -i)
                y_temp = y_new + d * x_new * (2 ** -i)
                z -= d * self.angle_table[i]
            elif mode == "linear":
              i = i-offset
              print(f"i={i}")
              x_temp = x_new  # x stays constant
              y_temp = y_new + d * x_new * (2 ** -i)
              # z -= d * math.degrees(2 ** -i)  # Correct: step is in radians converted to degrees
              z -= d * 2 ** -i
              # print(f"n={i+1}, d={d}, angle={z:.6f}, rotated angle = {math.degrees(2**-i):.6f}")
              # print(f"n={i+1}, d={d}, angle={z:.6f}, rotated angle = {2**-i:.6f}")
            else:
                raise ValueError("Mode must be 'circular' or 'linear'")

            x_new, y_new = x_temp, y_temp
            

        # Apply gain correction only in circular mode
        if mode == "circular":
            x_new *= self.K
            y_new *= self.K

        return x_new, y_new

    def vector(self, x, y):
        """
        Vectoring mode: Compute magnitude and angle of (x, y)
        """
        z = 0
        for i in range(self.iterations):
            d = 1 if y >= 0 else -1
            x_temp = x + d * y * (2 ** -i)
            y_temp = y - d * x * (2 ** -i)
            z += d * self.angle_table[i]
            x, y = x_temp, y_temp
        magnitude = x * self.K
        angle = z
        return magnitude, angle


# Simulation and error calculation
cordic = CORDIC(iterations=8)
angles_deg = list(range(1, 46))  # From 0° to 45°
x_input = 1.0
errors = []

for angle in angles_deg:
    expected = x_input * angle  # Expected y = x * angle (in degrees)
    _, y_cordic = cordic.rotate(x_input, 0.0, angle, mode="linear", offset=math.ceil(math.log2(angle)))
    error = abs((y_cordic - expected) / expected) * 100 if expected != 0 else 0
    print(f"Angle: {angle}°, Expected: {expected:.6f}, CORDIC: {y_cordic:.6f}, Error: {error:.6f}%")
    errors.append(error)

# Plot error
plt.figure(figsize=(10, 6))
plt.plot(angles_deg, errors, marker='o')
plt.title("Error Rate vs Input Angle (Linear Mode CORDIC)")
plt.xlabel("Input Angle (degrees)")
plt.ylabel("Error (%)")
plt.grid(True)
plt.tight_layout()

plt.show()
