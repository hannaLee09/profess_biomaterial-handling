"""
step2_volume.py — Volume Estimation via Numerical Integration (Image-Based)
===========================================================================
Loads the avocado profile extracted from the reference image, applies cubic
spline interpolation, and computes the volume of revolution using Simpson's
and Trapezoidal rules.

Run: python step2_volume.py
Dependencies: pip install numpy scipy opencv-python
"""
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import simpson, trapezoid

# ============================================================
# Step 2-A: Load Profile Data from Avocado Image
# ============================================================
from avocado_profile import extract_profile

data = extract_profile()
x_points = data['x_points']      # Points for spline fitting (~15+)
r_points = data['r_points']
x_textbook = data['x_textbook']   # Textbook reference points (6)
r_textbook = data['r_textbook']

source = 'Image-based' if data['from_image'] else 'Textbook data'
print(f"[Data Source] {source}")

cs = CubicSpline(x_points, r_points, bc_type='natural')

# ============================================================
# Step 2-B: Integration Precision vs. Subdivision Count
# ============================================================
print("\n" + "=" * 60)
print(f"Volume Estimation by Subdivision Count (n) [{source}]")
print("=" * 60)
print(f"{'n':>10} | {'Simpson [cm³]':>15} | {'Trapezoidal [cm³]':>18} | {'Diff [cm³]':>12}")
print("-" * 60)

L = x_points[-1]

for n in [10, 20, 50, 100, 500, 1000]:
    x_new = np.linspace(0, L, n)
    r_new = cs(x_new)
    r_new = np.maximum(r_new, 0)

    areas = np.pi * (r_new ** 2)
    vol_simpson = simpson(areas, x=x_new)
    vol_trapezoid = trapezoid(areas, x=x_new)
    diff = abs(vol_simpson - vol_trapezoid)
    print(f"{n:>10} | {vol_simpson:>15.4f} | {vol_trapezoid:>18.4f} | {diff:>12.6f}")

# ============================================================
# Step 2-C: Final Volume Estimation (n=100)
# ============================================================
print("\n" + "=" * 60)
print(f"Final Volume Estimation (n = 100) [{source}]")
print("=" * 60)

x_final = np.linspace(0, L, 100)
r_final = cs(x_final)
r_final = np.maximum(r_final, 0)
areas_final = np.pi * (r_final ** 2)

vol_simpson_final = simpson(areas_final, x=x_final)
vol_trapezoid_final = trapezoid(areas_final, x=x_final)

vol_manual = 334.1  # cm³ (textbook manual calculation)

print(f"  Simpson's Rule   : {vol_simpson_final:.4f} cm³")
print(f"  Trapezoidal Rule : {vol_trapezoid_final:.4f} cm³")
print(f"  Manual (textbook): {vol_manual:.1f} cm³ (5-segment)")

if vol_manual > 0:
    err_simpson = abs(vol_simpson_final - vol_manual) / vol_manual * 100
    err_trap = abs(vol_trapezoid_final - vol_manual) / vol_manual * 100
    print(f"\n  Simpson  vs manual diff: {err_simpson:.2f}%")
    print(f"  Trapezoid vs manual diff: {err_trap:.2f}%")

if data['from_image']:
    print(f"\n[Note] The image-extracted profile may differ from the textbook")
    print(f"       manual calculation depending on the actual specimen shape.")

print("\n[Discussion] As n increases, the difference between Simpson and")
print("             Trapezoidal converges to zero. Both methods converge")
print("             to a stable volume estimate. Simpson's Rule uses")
print("             parabolic approximation, providing higher accuracy")
print("             than Trapezoidal at the same subdivision count.")
