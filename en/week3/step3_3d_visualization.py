"""
step3_3d_visualization.py — Image-Based 3D Surface Reconstruction & Visualization
===================================================================================
Reconstructs a 3D solid of revolution from the image-extracted avocado profile
and displays volume/surface area results alongside the original image.

Run: python step3_3d_visualization.py
Dependencies: pip install numpy scipy matplotlib opencv-python
"""
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import simpson
import matplotlib.pyplot as plt
import cv2
from mpl_toolkits.mplot3d import Axes3D

# ============================================================
# Step 3-A: Load Profile Data from Avocado Image
# ============================================================
from avocado_profile import extract_profile

data = extract_profile()
x_points = data['x_points']      # Points for spline fitting (~15+)
r_points = data['r_points']
x_textbook = data['x_textbook']   # Textbook reference points (6)
r_textbook = data['r_textbook']

source = 'Image-based' if data['from_image'] else 'Textbook data'

cs = CubicSpline(x_points, r_points, bc_type='natural')
L = x_points[-1]

x_new = np.linspace(0, L, 100)
r_new = cs(x_new)
r_new = np.maximum(r_new, 0)

# ============================================================
# Step 3-B: Volume & Surface Area Calculation
# ============================================================
areas = np.pi * (r_new ** 2)
volume = simpson(areas, x=x_new)

dr_dx = cs(x_new, 1)
surface_integrand = 2 * np.pi * r_new * np.sqrt(1 + dr_dx ** 2)
surface_area = simpson(surface_integrand, x=x_new)

print("=" * 50)
print(f"Avocado 3D Reconstruction Results [{source}]")
print("=" * 50)
print(f"  Estimated Volume       : {volume:.2f} cm³")
print(f"  Estimated Surface Area : {surface_area:.2f} cm²")
print(f"  Specific Surface       : {surface_area / volume:.4f} cm⁻¹")
print("=" * 50)

# ============================================================
# Step 3-C: 3D Mesh Generation
# ============================================================
theta = np.linspace(0, 2 * np.pi, 50)
X, THETA = np.meshgrid(x_new, theta)
R = cs(X)
R = np.maximum(R, 0)
Y = R * np.cos(THETA)
Z = R * np.sin(THETA)

# ============================================================
# Step 3-D: Visualization (Original Image + 3D + 2D Profile)
# ============================================================
if data['from_image'] and data['image'] is not None:
    fig = plt.figure(figsize=(18, 6))

    # [Left] Original image + contour
    ax0 = fig.add_subplot(131)
    img_rgb = cv2.cvtColor(data['image'], cv2.COLOR_BGR2RGB)
    img_show = img_rgb.copy()
    cv2.drawContours(img_show, [data['contour']], -1, (255, 0, 0), 3)
    ax0.imshow(img_show)
    ax0.set_title('Input Image', fontsize=12)
    ax0.axis('off')

    # [Center] 3D surface
    ax1 = fig.add_subplot(132, projection='3d')
    ax1.plot_surface(X, Y, Z, cmap='YlGn', alpha=0.8, edgecolor='none')
    ax1.set_xlabel('Length x [cm]')
    ax1.set_ylabel('Y [cm]')
    ax1.set_zlabel('Z [cm]')
    ax1.set_title(f'3D Reconstruction\nV={volume:.1f} cm³', fontsize=11)
    ax1.set_box_aspect([2, 1, 1])

    # [Right] 2D cross-section
    ax2 = fig.add_subplot(133)
    ax2.fill_between(x_new, r_new, -r_new, alpha=0.3, color='green',
                     label='Revolution cross-section')
    ax2.plot(x_new, r_new, 'g-', linewidth=2)
    ax2.plot(x_new, -r_new, 'g-', linewidth=2)
    ax2.plot(x_textbook, r_textbook, 'ro', markersize=8, label='Sample points')
    ax2.plot(x_textbook, -r_textbook, 'ro', markersize=8)
    for xp in x_textbook:
        ax2.axvline(x=xp, color='gray', linestyle='--', alpha=0.3)
    ax2.set_xlabel('Length x [cm]')
    ax2.set_ylabel('Radius r [cm]')
    ax2.set_title(f'2D Profile (S={surface_area:.1f} cm²)', fontsize=11)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_aspect('equal')

    plt.suptitle('Step 3: Image → Profile → 3D Solid of Revolution',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

else:
    fig = plt.figure(figsize=(14, 5))

    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot_surface(X, Y, Z, cmap='YlGn', alpha=0.8, edgecolor='none')
    ax1.set_xlabel('Length x [cm]')
    ax1.set_ylabel('Y [cm]')
    ax1.set_zlabel('Z [cm]')
    ax1.set_title(f'Reconstructed 3D Avocado\nV = {volume:.1f} cm³, S = {surface_area:.1f} cm²')
    ax1.set_box_aspect([2, 1, 1])

    ax2 = fig.add_subplot(122)
    ax2.fill_between(x_new, r_new, -r_new, alpha=0.3, color='green',
                     label='Revolution cross-section')
    ax2.plot(x_new, r_new, 'g-', linewidth=2)
    ax2.plot(x_new, -r_new, 'g-', linewidth=2)
    ax2.plot(x_textbook, r_textbook, 'ro', markersize=8, label='Sample points')
    ax2.plot(x_textbook, -r_textbook, 'ro', markersize=8)
    for xp in x_textbook:
        ax2.axvline(x=xp, color='gray', linestyle='--', alpha=0.3)
    ax2.set_xlabel('Length x [cm]')
    ax2.set_ylabel('Radius r [cm]')
    ax2.set_title('2D Profile Cross-section')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_aspect('equal')

    plt.tight_layout()
    plt.show()
