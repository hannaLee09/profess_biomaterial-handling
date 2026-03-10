import numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import simpson
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ============================================================
# Step 3: 3D 회전체 표면 재구성 및 시각화
# ============================================================
# Step 1의 보간 곡선 r(x)를 중심축(x축) 주위로 360도 회전시켜
# 3D 표면을 재구성하고, 추정된 체적·표면적을 함께 표출합니다.

# --- 데이터 준비 ---
x_points = np.array([0, 1.0, 5.0, 6.5, 8.0, 10.85])
r_points = np.array([0, 1.47, 3.185, 3.38, 3.04, 0])

cs = CubicSpline(x_points, r_points, bc_type='natural')

x_new = np.linspace(0, 10.85, 100)
r_new = cs(x_new)
r_new = np.maximum(r_new, 0)

# --- 체적 계산 ---
areas = np.pi * (r_new ** 2)
volume = simpson(areas, x=x_new)

# --- 표면적 계산 (회전체 표면적 공식) ---
# S = 2π ∫ r(x) × √(1 + (dr/dx)²) dx
dr_dx = cs(x_new, 1)  # 1차 도함수 (기울기)
surface_integrand = 2 * np.pi * r_new * np.sqrt(1 + dr_dx ** 2)
surface_area = simpson(surface_integrand, x=x_new)

print("=" * 50)
print("아보카도 3D 형상 재구성 결과")
print("=" * 50)
print(f"  추정 체적    : {volume:.2f} cm³")
print(f"  추정 표면적  : {surface_area:.2f} cm²")
print(f"  비표면적     : {surface_area / volume:.4f} cm⁻¹")
print("=" * 50)

# --- 3D 회전체 메시(Mesh) 생성 ---
theta = np.linspace(0, 2 * np.pi, 50)   # 회전각 (0 ~ 360도)
X, THETA = np.meshgrid(x_new, theta)    # 2D 그리드

# 원통 좌표 → 직교 좌표 변환
R = cs(X)
R = np.maximum(R, 0)
Y = R * np.cos(THETA)
Z = R * np.sin(THETA)

# --- 3D 시각화 ---
fig = plt.figure(figsize=(14, 5))

# [좌측] 3D 표면 플롯
ax1 = fig.add_subplot(121, projection='3d')
ax1.plot_surface(X, Y, Z, cmap='YlGn', alpha=0.8, edgecolor='none')
ax1.set_xlabel('길이 x [cm]')
ax1.set_ylabel('Y [cm]')
ax1.set_zlabel('Z [cm]')
ax1.set_title(f'3D 재구성 아보카도\nV = {volume:.1f} cm³, S = {surface_area:.1f} cm²')
ax1.set_box_aspect([2, 1, 1])

# [우측] 2D 단면 프로파일 + 적분 영역
ax2 = fig.add_subplot(122)
ax2.fill_between(x_new, r_new, -r_new, alpha=0.3, color='green', label='회전체 단면')
ax2.plot(x_new, r_new, 'g-', linewidth=2)
ax2.plot(x_new, -r_new, 'g-', linewidth=2)
ax2.plot(x_points, r_points, 'ro', markersize=8, label='측정 포인트')
ax2.plot(x_points, -r_points, 'ro', markersize=8)

# 적분 구간 표시 (세로 점선)
for xp in x_points:
    ax2.axvline(x=xp, color='gray', linestyle='--', alpha=0.3)

ax2.set_xlabel('길이 x [cm]')
ax2.set_ylabel('반지름 r [cm]')
ax2.set_title('2D 프로파일 단면')
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_aspect('equal')

plt.tight_layout()
plt.show()
