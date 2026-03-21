# -*- coding: utf-8 -*-
"""
Biomaterial Handling & Processing - Week 04 Lab
Topic: Calculation and Visualization of Density & Porosity for Agricultural Products

This script uses the individual avocado volume data derived from the Week 3 lab,
along with virtual mass and packaging box data, to calculate the 'Particle Density', 
'Bulk Density', and 'Porosity'. It then visualizes the results.
"""

import numpy as np
import matplotlib.pyplot as plt
from itertools import product, combinations
from scipy.spatial.distance import cdist  # ADDED: For spatial distance calculation

# User-specific Font Setting for Matplotlib Title & Labels (e.g., Windows OS)
plt.rcParams['font.family'] = 'Segoe UI'
plt.rcParams['axes.unicode_minus'] = False

# =====================================================================
# [Step 1] Individual Object (1 Avocado) Volume & Mass (Particle Density)
# =====================================================================
# Individual avocado volume derived from Week 3 (approx. 205.4 cm^3 via Simpson)
volume_single_cm3 = 205.4
# Hypothetical individual mass measurement (e.g., via digital scale, 215.0 g)
mass_single_g = 215.0

# Calculate Particle Density
density_particle = mass_single_g / volume_single_cm3

print(f"{'='*50}")
print(f"[Step 1] Individual Object Density (Particle Density)")
print(f"{'='*50}")
print(f" - Single Volume : {volume_single_cm3:>8.2f} cm^3")
print(f" - Single Mass   : {mass_single_g:>8.2f} g")
print(f" -> Particle Density: {density_particle:>8.3f} g/cm^3")
print(f"    (Expected to sink as it is > water density 1.0)")

# =====================================================================
# [Step 2] Density of Entire Payload in Packing Box (Bulk Density)
# =====================================================================
# Standard plastic logistics crate dimensions (L 40cm * W 30cm * H 15cm)
box_volume_cm3 = 40.0 * 30.0 * 15.0  # 18,000 cm^3
# Total number of avocados loaded in the box
avocado_count = 45

# Total mass (Single mass * Count)
mass_total_g = mass_single_g * avocado_count

# Bulk Density based on the entire box volume
density_bulk = mass_total_g / box_volume_cm3

print(f"\n{'='*50}")
print(f"[Step 2] Packed Cargo Density (Bulk Density)")
print(f"{'='*50}")
print(f" - Total Box Volume: {box_volume_cm3:>8.2f} cm^3")
print(f" - Loaded Count    : {avocado_count:>8} units")
print(f" - Total Mass      : {mass_total_g:>8.2f} g")
print(f" -> Bulk Density   : {density_bulk:>8.3f} g/cm^3")

# =====================================================================
# [Step 3] Porosity Cross-Validation Calculation
# =====================================================================
# Method A: Density Ratio based formula
# Porosity = 1 - (Bulk Density / Particle Density)
porosity_density_based = (1 - (density_bulk / density_particle)) * 100

# Method B: Physical Volume Subtraction
# Actual Void Volume = Total Box Volume - (Single Volume * Count)
void_volume = box_volume_cm3 - (volume_single_cm3 * avocado_count)
porosity_volume_based = (void_volume / box_volume_cm3) * 100

print(f"\n{'='*50}")
print(f"[Step 3] Porosity Derivation & Cross-Validation")
print(f"{'='*50}")
print(f" A. Density Ratio Porosity  : {porosity_density_based:>6.2f} %")
print(f" B. Volume Subtrct Porosity : {porosity_volume_based:>6.2f} %")
if abs(porosity_density_based - porosity_volume_based) < 1e-5:
    print(f" -> [Success] Both formulas match perfectly.")
else:
    print(f" -> [Failure] Discrepancy detected.")

# =====================================================================
# [Step 4] Visualization (3D Packing / Bar / Pie Chart)
# =====================================================================
fig = plt.figure(figsize=(18, 6))

# ---- (A) Left: 3D Virtual Packing Simulation (Spatial Intuition) ----
ax1 = fig.add_subplot(131, projection='3d')

# Draw 40x30x15 box wireframe
r = [0, 40]
for s, e in combinations(np.array(list(product(r, [0, 30], [0, 15]))), 2):
    if np.sum(np.abs(s-e)) in [40, 30, 15]:
        ax1.plot3D(*zip(s, e), color="black", linestyle='--', alpha=0.3)

# Place 45 avocados in a virtual grid (5x3x3)
x_centers = np.linspace(4, 36, 5)
y_centers = np.linspace(5, 25, 3)
z_centers = np.linspace(2.5, 12.5, 3)
X, Y, Z = np.meshgrid(x_centers, y_centers, z_centers)

# Plot avocados as 3D Scatters (adjust size and color)
ax1.scatter(X, Y, Z, s=600, c='#8BC34A', alpha=0.9, edgecolors='#33691E', label='Avocado')

# [NEW] Intuitive Void Visualization: Generate point cloud for empty spaces
res = 1.5
vx, vy, vz = np.meshgrid(np.arange(0, 40, res), np.arange(0, 30, res), np.arange(0, 15, res))
pts = np.vstack([vx.flatten(), vy.flatten(), vz.flatten()]).T
centers = np.vstack([X.flatten(), Y.flatten(), Z.flatten()]).T

distances = cdist(pts, centers)
min_distances = np.min(distances, axis=1)

# Mask points that are further than ~3.0cm from avocado centroids as 'Void'
void_mask = min_distances > 3.0
void_pts = pts[void_mask]

# Sub-sample 80% to retain performance
sub_sample_size = int(len(void_pts) * 0.8)
if sub_sample_size > 0:
    idx = np.random.choice(len(void_pts), sub_sample_size, replace=False)
    v_pts_sub = void_pts[idx]
    # Represent void as red semi-transparent cubes
    ax1.scatter(v_pts_sub[:,0], v_pts_sub[:,1], v_pts_sub[:,2], 
                s=40, c='#FF0000', alpha=0.3, marker='s', edgecolors='none', label='Void')

ax1.set_title('Step 4-a: 3D Virtual Packing & Voids', fontsize=14, pad=15)
ax1.set_xlabel('Length (40cm)')
ax1.set_ylabel('Width (30cm)')
ax1.set_zlabel('Height (15cm)')
ax1.set_box_aspect((40, 30, 15))  # Correct box ratio
ax1.legend(loc='upper right', fontsize=10)

# ---- (B) Center: Density Comparison Bar Chart ----
ax2 = fig.add_subplot(132)
labels = ['Individual Particle\n(Density)', 'Cargo Bulk\n(Density)']
values = [density_particle, density_bulk]
colors = ['#0056b3', '#80bfff']

bars = ax2.bar(labels, values, color=colors, width=0.5, edgecolor='black')
ax2.set_ylabel('Density [g/cm³]', fontsize=12)
ax2.set_title('Step 4-b: Gap Analysis (Particle vs Bulk)', fontsize=14, pad=15)
ax2.set_ylim(0, max(values) * 1.3)
ax2.grid(axis='y', linestyle='--', alpha=0.5)

# Display numerical texts above bars
for bar in bars:
    y_val = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, y_val + 0.03, 
             f'{y_val:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=11)

# ---- (C) Right: Box Internal Volume Pie Chart ----
ax3 = fig.add_subplot(133)
pie_labels = ['Avocado Volume\n(Occupied Space)', 'Empty Void Gap\n(Porosity)']
pie_sizes = [100 - porosity_density_based, porosity_density_based]
pie_colors = ['#8BC34A', '#e6f0ff']
explode = (0.05, 0) # Explode the avocado section for standout effect

ax3.pie(pie_sizes, explode=explode, labels=pie_labels, colors=pie_colors,
        autopct='%1.1f%%', shadow=False, startangle=140, 
        textprops={'fontsize': 13, 'fontweight': 'bold'},
        wedgeprops={'edgecolor': 'black', 'linewidth': 1})
ax3.set_title(f'Step 4-c: Volume Occupancy & Porosity ({avocado_count} Units)', fontsize=14, pad=15)

# Layout tuning to prevent UI interference and screen display
plt.tight_layout()
plt.show()
