"""
step1_interpolation.py — Image-Based Profile Extraction & Cubic Spline Interpolation
=====================================================================================
Automatically extracts the avocado contour from the reference image
(images/avocado_front_view.png) using OpenCV, then generates a smooth
profile curve via cubic spline interpolation.

Run: python step1_interpolation.py
Dependencies: pip install numpy scipy matplotlib opencv-python
"""
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import cv2

# ============================================================
# Step 1-A: Automatic Profile Data Extraction from Avocado Image
# ============================================================
from avocado_profile import extract_profile

data = extract_profile()
x_points = data['x_points']      # Points for spline fitting (~15+)
r_points = data['r_points']
x_textbook = data['x_textbook']   # Textbook reference points (6)
r_textbook = data['r_textbook']

source = 'Image-based' if data['from_image'] else 'Textbook data'
print(f"\n{'='*50}")
print(f"Extracted Profile Data [{source}]")
print(f"{'='*50}")
print(f"Spline fitting points: {len(x_points)}")
print(f"Textbook reference points:")
for i, (x, r) in enumerate(zip(x_textbook, r_textbook)):
    print(f"  Point {i+1}: x = {x:6.2f} cm,  r = {r:6.3f} cm")

# ============================================================
# Step 1-B: Cubic Spline Interpolation
# ============================================================
cs = CubicSpline(x_points, r_points, bc_type='natural')
x_new = np.linspace(0, x_points[-1], 100)
r_new = cs(x_new)
r_new = np.maximum(r_new, 0)  # Correct negative radii

# ============================================================
# Step 1-C: Visualization — Original Image + Profile Comparison
# ============================================================
if data['from_image'] and data['image'] is not None:
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # [Left] Original image + detected contour
    ax1 = axes[0]
    img_rgb = cv2.cvtColor(data['image'], cv2.COLOR_BGR2RGB)
    img_contour = img_rgb.copy()
    cv2.drawContours(img_contour, [data['contour']], -1, (255, 0, 0), 3)
    ax1.imshow(img_contour)
    ax1.set_title('Original Image + Detected Contour', fontsize=12)
    ax1.axis('off')

    # [Center] Binarization result
    ax2 = axes[1]
    ax2.imshow(data['binary'], cmap='gray')
    ax2.set_title('Otsu Binarization + Morphology', fontsize=12)
    ax2.axis('off')

    # [Right] Extracted profile + spline interpolation
    ax3 = axes[2]
    if data['x_dense'] is not None:
        ax3.fill_between(data['x_dense'], data['r_dense'], -data['r_dense'],
                         alpha=0.15, color='blue', label='Image-extracted profile')
    ax3.fill_between(x_new, r_new, -r_new, alpha=0.3, color='green',
                     label='Cubic Spline interpolation')
    ax3.plot(x_new, r_new, 'g-', linewidth=2)
    ax3.plot(x_new, -r_new, 'g-', linewidth=2)
    ax3.plot(x_textbook, r_textbook, 'ro', markersize=8, label='Textbook reference points')
    ax3.plot(x_textbook, -r_textbook, 'ro', markersize=8)
    ax3.plot(x_points, r_points, 'b^', markersize=5, alpha=0.5, label='Spline fit points')
    ax3.set_xlabel('Position x [cm]', fontsize=11)
    ax3.set_ylabel('Radius r [cm]', fontsize=11)
    ax3.set_title('Extracted Profile → Cubic Spline', fontsize=12)
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)
    ax3.set_aspect('equal')

    plt.suptitle('Step 1: Image → Profile Extraction → Spline Interpolation',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

else:
    plt.figure(figsize=(10, 5))
    plt.fill_between(x_new, r_new, -r_new, alpha=0.3, color='green',
                     label='Interpolated Cross-section')
    plt.plot(x_new, r_new, 'g-', linewidth=2)
    plt.plot(x_new, -r_new, 'g-', linewidth=2)
    plt.plot(x_textbook, r_textbook, 'ro', markersize=8, label='Measured Data')
    plt.plot(x_textbook, -r_textbook, 'ro', markersize=8)
    plt.xlabel('Position x [cm]', fontsize=12)
    plt.ylabel('Radius r [cm]', fontsize=12)
    plt.title('Step 1: Avocado Profile - Cubic Spline Interpolation', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

print(f"\nSpline fitting points: {len(x_points)}")
print(f"Textbook reference points: {len(x_textbook)}")
print(f"Interpolated points: {len(x_new)}")
print(f"Total avocado length: {x_points[-1]:.2f} cm")
print(f"Max radius: {r_points.max():.3f} cm")
