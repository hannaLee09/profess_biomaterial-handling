import numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import simpson, trapezoid

# ============================================================
# Step 2: Volume Estimation via Numerical Integration
#         (Simpson's Rule vs. Trapezoidal Rule)
# ============================================================
# Rotate the interpolated profile curve r(x) from Step 1 around
# the central axis to compute the volume of revolution.
# Volume formula: V = π ∫ r(x)² dx

# --- Data Preparation (same as Step 1) ---
x_points = np.array([0, 1.0, 5.0, 6.5, 8.0, 10.85])
r_points = np.array([0, 1.47, 3.185, 3.38, 3.04, 0])

cs = CubicSpline(x_points, r_points, bc_type='natural')

# --- Comparing integration precision across subdivisions (n) ---
print("=" * 60)
print("Volume Estimation by Number of Subdivisions (n)")
print("=" * 60)
print(f"{'n':>10} | {'Simpson [cm³]':>15} | {'Trapezoidal [cm³]':>18} | {'Diff [cm³]':>12}")
print("-" * 60)

for n in [10, 20, 50, 100, 500, 1000]:
    x_new = np.linspace(0, 10.85, n)
    r_new = cs(x_new)
    r_new = np.maximum(r_new, 0)  # Correct negative radii
    
    # Cross-sectional area: A(x) = π × r(x)²
    areas = np.pi * (r_new ** 2)
    
    # Simpson's Rule — parabolic approximation
    vol_simpson = simpson(areas, x=x_new)
    
    # Trapezoidal Rule — linear approximation
    vol_trapezoid = trapezoid(areas, x=x_new)
    
    diff = abs(vol_simpson - vol_trapezoid)
    print(f"{n:>10} | {vol_simpson:>15.4f} | {vol_trapezoid:>18.4f} | {diff:>12.6f}")

# --- Final volume calculation (n=100, compared with textbook) ---
print("\n" + "=" * 60)
print("Final Volume Estimation Results (n = 100)")
print("=" * 60)

x_final = np.linspace(0, 10.85, 100)
r_final = cs(x_final)
r_final = np.maximum(r_final, 0)
areas_final = np.pi * (r_final ** 2)

vol_simpson_final = simpson(areas_final, x=x_final)
vol_trapezoid_final = trapezoid(areas_final, x=x_final)

# Textbook Example 3-3 manual segmentation result (reference value)
vol_manual = 334.1  # cm³ (5-segment manual calculation, approximate)

print(f"  Simpson's Rule   : {vol_simpson_final:.4f} cm³")
print(f"  Trapezoidal Rule : {vol_trapezoid_final:.4f} cm³")
print(f"  Textbook manual  : {vol_manual:.1f} cm³ (5-segment calculation)")

if vol_manual > 0:
    err_simpson = abs(vol_simpson_final - vol_manual) / vol_manual * 100
    err_trap = abs(vol_trapezoid_final - vol_manual) / vol_manual * 100
    print(f"\n  Simpson  vs manual diff: {err_simpson:.2f}%")
    print(f"  Trapezoid vs manual diff: {err_trap:.2f}%")

print("\n[Discussion] As the number of subdivisions increases, the difference")
print("             between Simpson and Trapezoidal converges to zero.")
print("             Simpson's Rule uses parabolic approximation, providing")
print("             higher accuracy than Trapezoidal at the same subdivision count.")
