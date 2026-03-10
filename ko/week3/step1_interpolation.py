import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

# ============================================================
# Step 1: 아보카도 프로파일 데이터 입력 및 큐빅 스플라인 보간
# ============================================================
# 교재 예제 3-3에서 제공된 아보카도의 길이 방향 위치(x)와
# 각 위치에서의 반지름(r) 측정값을 배열로 입력합니다.

# 측정 데이터 (위치 x [cm], 반지름 r [cm])
x_points = np.array([0, 1.0, 5.0, 6.5, 8.0, 10.85])   # 길이 방향 위치
r_points = np.array([0, 1.47, 3.185, 3.38, 3.04, 0])   # 각 위치의 반지름

# 큐빅 스플라인 보간 (Cubic Spline Interpolation)
# - 6개의 이산 측정 포인트를 매끄러운 연속 곡선으로 변환
# - bc_type='natural': 양 끝단에서 2차 도함수 = 0 (자연 경계 조건)
cs = CubicSpline(x_points, r_points, bc_type='natural')

# 보간된 곡선을 위한 세밀한 x 좌표 생성 (100개 포인트)
x_new = np.linspace(0, 10.85, 100)
r_new = cs(x_new)

# 음수 반지름 보정 (보간 특성상 양 끝에서 미세하게 음수가 될 수 있음)
r_new = np.maximum(r_new, 0)

# ============================================================
# 시각화: 원본 측정점과 보간 곡선 비교
# ============================================================
plt.figure(figsize=(10, 5))

# 보간 곡선 (상하 대칭으로 회전체 단면 표현)
plt.fill_between(x_new, r_new, -r_new, alpha=0.3, color='green', label='보간 단면 (Interpolated Cross-section)')
plt.plot(x_new, r_new, 'g-', linewidth=2)
plt.plot(x_new, -r_new, 'g-', linewidth=2)

# 원본 측정 포인트
plt.plot(x_points, r_points, 'ro', markersize=8, label='측정 데이터 (Measured Data)')
plt.plot(x_points, -r_points, 'ro', markersize=8)

plt.xlabel('길이 방향 위치 x [cm]', fontsize=12)
plt.ylabel('반지름 r [cm]', fontsize=12)
plt.title('Step 1: 아보카도 프로파일 - 큐빅 스플라인 보간', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.axis('equal')
plt.tight_layout()
plt.show()

print(f"측정 포인트 수: {len(x_points)}개")
print(f"보간 후 포인트 수: {len(x_new)}개")
print(f"아보카도 전체 길이: {x_points[-1]:.2f} cm")
print(f"최대 반지름: {r_points.max():.3f} cm (위치: x = {x_points[r_points.argmax()]:.1f} cm)")
