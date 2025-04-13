import math

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

    def rotate(self, x, y, angle_deg, mode="circular"):
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
              i = i-5
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


if __name__ == "__main__":
    cordic = CORDIC(iterations=8)

    # === Rotation Mode Test ===
    x, y = 1.0, 0.0
    angle = 45  # degrees

    x_circ, y_circ = cordic.rotate(x, y, angle, mode="circular")
    print(f"[Circular] Rotate ({x}, {y}) by {angle}°: ({x_circ:.6f}, {y_circ:.6f})")

    x_lin, y_lin = cordic.rotate(x, y, angle, mode="linear")
    print(f"[Linear  ] Rotate ({x}, {y}) by {angle}° (linear): ({x_lin:.6f}, {y_lin:.6f})")

    # === Vector Mode Test ===
    x_vec, y_vec = 0.7071, 0.7071
    mag, ang = cordic.vector(x_vec, y_vec)
    print(f"[Vectoring] ({x_vec}, {y_vec}): Magnitude = {mag:.6f}, Angle = {ang:.6f}°")
