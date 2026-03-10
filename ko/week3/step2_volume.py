import numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import simpson, trapezoid

# ============================================================
# Step 2: 수치 적분을 이용한 체적 추정 (Simpson vs. Trapezoidal)
# ============================================================
# Step 1에서 생성한 보간 곡선 r(x)를 중심축 주위로 회전시켜
# 회전체의 체적을 수치 적분으로 산출합니다.
# 체적 공식: V = π ∫ r(x)² dx

# --- 데이터 준비 (Step 1과 동일) ---
x_points = np.array([0, 1.0, 5.0, 6.5, 8.0, 10.85])
r_points = np.array([0, 1.47, 3.185, 3.38, 3.04, 0])

cs = CubicSpline(x_points, r_points, bc_type='natural')

# --- 분할 수(n)에 따른 적분 정밀도 비교 ---
print("=" * 60)
print("분할 수(n)에 따른 체적 추정값 비교")
print("=" * 60)
print(f"{'분할 수(n)':>10} | {'Simpson [cm³]':>15} | {'Trapezoidal [cm³]':>18} | {'차이 [cm³]':>12}")
print("-" * 60)

for n in [10, 20, 50, 100, 500, 1000]:
    x_new = np.linspace(0, 10.85, n)
    r_new = cs(x_new)
    r_new = np.maximum(r_new, 0)  # 음수 반지름 보정
    
    # 단면적 계산: A(x) = π × r(x)²
    areas = np.pi * (r_new ** 2)
    
    # 심슨 공식 (Simpson's Rule) - 포물선 근사
    vol_simpson = simpson(areas, x=x_new)
    
    # 사다리꼴 공식 (Trapezoidal Rule) - 직선 근사
    vol_trapezoid = trapezoid(areas, x=x_new)
    
    diff = abs(vol_simpson - vol_trapezoid)
    print(f"{n:>10} | {vol_simpson:>15.4f} | {vol_trapezoid:>18.4f} | {diff:>12.6f}")

# --- 최종 체적 산출 (n=100 기준, 교재 예제와 비교) ---
print("\n" + "=" * 60)
print("최종 체적 추정 결과 (n = 100)")
print("=" * 60)

x_final = np.linspace(0, 10.85, 100)
r_final = cs(x_final)
r_final = np.maximum(r_final, 0)
areas_final = np.pi * (r_final ** 2)

vol_simpson_final = simpson(areas_final, x=x_final)
vol_trapezoid_final = trapezoid(areas_final, x=x_final)

# 교재 예제 3-3의 수동 분할 계산 결과 (참고값)
vol_manual = 334.1  # cm³ (교재 상 5개 구간 분할 계산값, 근사)

print(f"  Simpson's Rule   : {vol_simpson_final:.4f} cm³")
print(f"  Trapezoidal Rule : {vol_trapezoid_final:.4f} cm³")
print(f"  교재 수동 계산값  : {vol_manual:.1f} cm³ (5개 구간 분할)")

if vol_manual > 0:
    err_simpson = abs(vol_simpson_final - vol_manual) / vol_manual * 100
    err_trap = abs(vol_trapezoid_final - vol_manual) / vol_manual * 100
    print(f"\n  Simpson  vs 수동계산 차이: {err_simpson:.2f}%")
    print(f"  Trapezoid vs 수동계산 차이: {err_trap:.2f}%")

print("\n[고찰] 분할 수가 증가할수록 Simpson과 Trapezoidal의 차이가")
print("       0에 수렴하며, 두 방법 모두 안정적인 체적값으로 수렴합니다.")
print("       Simpson 공식은 2차 포물선 근사를 사용하므로 동일한 분할 수에서")
print("       Trapezoidal보다 높은 정확도를 보입니다.")
