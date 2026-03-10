import numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import simpson
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ============================================================
# Step 3: 3D Surface Reconstruction of Solid of Revolution
# ============================================================
# Rotate the interpolated profile curve r(x) from Step 1
# around the central axis (x-axis) by 360 degrees to reconstruct
# the 3D surface, and display the estimated volume and surface area.

# --- Data Preparation ---
x_points = np.array([0, 1.0, 5.0, 6.5, 8.0, 10.85])
r_points = np.array([0, 1.47, 3.185, 3.38, 3.04, 0])

cs = CubicSpline(x_points, r_points, bc_type='natural')

x_new = np.linspace(0, 10.85, 100)
r_new = cs(x_new)
r_new = np.maximum(r_new, 0)

# --- Volume Calculation ---
areas = np.pi * (r_new ** 2)
volume = simpson(areas, x=x_new)

# --- Surface Area Calculation (Surface of Revolution Formula) ---
# S = 2π ∫ r(x) × √(1 + (dr/dx)²) dx
dr_dx = cs(x_new, 1)  # First derivative (slope)
surface_integrand = 2 * np.pi * r_new * np.sqrt(1 + dr_dx ** 2)
surface_area = simpson(surface_integrand, x=x_new)

print("=" * 50)
print("Avocado 3D Shape Reconstruction Results")
print("=" * 50)
print(f"  Estimated Volume       : {volume:.2f} cm³")
print(f"  Estimated Surface Area : {surface_area:.2f} cm²")
print(f"  Specific Surface       : {surface_area / volume:.4f} cm⁻¹")
print("=" * 50)

# --- 3D Rotational Surface Mesh Generation ---
theta = np.linspace(0, 2 * np.pi, 50)   # Rotation angle (0 – 360°)
X, THETA = np.meshgrid(x_new, theta)    # 2D grid

# Cylindrical → Cartesian coordinate conversion
R = cs(X)
R = np.maximum(R, 0)
Y = R * np.cos(THETA)
Z = R * np.sin(THETA)

# --- 3D Visualization ---
fig = plt.figure(figsize=(14, 5))

# [Left] 3D Surface Plot
ax1 = fig.add_subplot(121, projection='3d')
ax1.plot_surface(X, Y, Z, cmap='YlGn', alpha=0.8, edgecolor='none')
ax1.set_xlabel('Length x [cm]')
ax1.set_ylabel('Y [cm]')
ax1.set_zlabel('Z [cm]')
ax1.set_title(f'3D Reconstructed Avocado\nV = {volume:.1f} cm³, S = {surface_area:.1f} cm²')
ax1.set_box_aspect([2, 1, 1])

# [Right] 2D Cross-Section Profile + Integration Region
ax2 = fig.add_subplot(122)
ax2.fill_between(x_new, r_new, -r_new, alpha=0.3, color='green', label='Revolution Cross-section')
ax2.plot(x_new, r_new, 'g-', linewidth=2)
ax2.plot(x_new, -r_new, 'g-', linewidth=2)
ax2.plot(x_points, r_points, 'ro', markersize=8, label='Measured Points')
ax2.plot(x_points, -r_points, 'ro', markersize=8)

# Show integration segment boundaries (vertical dashed lines)
for xp in x_points:
    ax2.axvline(x=xp, color='gray', linestyle='--', alpha=0.3)

ax2.set_xlabel('Length x [cm]')
ax2.set_ylabel('Radius r [cm]')
ax2.set_title('2D Profile Cross-Section')
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_aspect('equal')

plt.tight_layout()
plt.show()
