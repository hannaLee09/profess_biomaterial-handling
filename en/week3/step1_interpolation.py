import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

# ============================================================
# Step 1: Avocado Profile Data Input & Cubic Spline Interpolation
# ============================================================
# Input the avocado's lengthwise position (x) and radius (r)
# measurements from textbook Example 3-3.

# Measured data (position x [cm], radius r [cm])
x_points = np.array([0, 1.0, 5.0, 6.5, 8.0, 10.85])   # Lengthwise position
r_points = np.array([0, 1.47, 3.185, 3.38, 3.04, 0])   # Radius at each position

# Cubic Spline Interpolation
# - Converts 6 discrete measurement points into a smooth continuous curve
# - bc_type='natural': Second derivative = 0 at both endpoints (natural boundary)
cs = CubicSpline(x_points, r_points, bc_type='natural')

# Generate fine x-coordinates for the interpolated curve (100 points)
x_new = np.linspace(0, 10.85, 100)
r_new = cs(x_new)

# Correct negative radii (interpolation may produce slight negatives near endpoints)
r_new = np.maximum(r_new, 0)

# ============================================================
# Visualization: Compare original measurements with interpolated curve
# ============================================================
plt.figure(figsize=(10, 5))

# Interpolated curve (symmetric top/bottom to represent rotational cross-section)
plt.fill_between(x_new, r_new, -r_new, alpha=0.3, color='green', label='Interpolated Cross-section')
plt.plot(x_new, r_new, 'g-', linewidth=2)
plt.plot(x_new, -r_new, 'g-', linewidth=2)

# Original measurement points
plt.plot(x_points, r_points, 'ro', markersize=8, label='Measured Data')
plt.plot(x_points, -r_points, 'ro', markersize=8)

plt.xlabel('Lengthwise Position x [cm]', fontsize=12)
plt.ylabel('Radius r [cm]', fontsize=12)
plt.title('Step 1: Avocado Profile - Cubic Spline Interpolation', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.axis('equal')
plt.tight_layout()
plt.show()

print(f"Number of measurement points: {len(x_points)}")
print(f"Number of interpolated points: {len(x_new)}")
print(f"Total avocado length: {x_points[-1]:.2f} cm")
print(f"Maximum radius: {r_points.max():.3f} cm (at x = {x_points[r_points.argmax()]:.1f} cm)")
