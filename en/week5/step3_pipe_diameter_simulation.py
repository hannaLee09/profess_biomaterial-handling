"""
Week 5 Lab: Step 3 - Pipe Diameter(D) Optimization & Hagen-Poiseuille Economics Simulator
(Animation resolving Discussion Topic 2)
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.patches as patches

# Font Config
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(figsize=(12, 7))
plt.subplots_adjust(left=0.08, bottom=0.35, right=0.95, top=0.9, wspace=0.3, hspace=0.3)

# Subplot 1: Pipe cross-section and friction vectors
ax_pipe = plt.subplot(1, 2, 1)
ax_pipe.set_xlim(-0.15, 0.15)
ax_pipe.set_ylim(-0.15, 0.15)
ax_pipe.set_aspect('equal')
ax_pipe.set_title('Pipe Cross-section & Wall Friction (ΔP)', fontsize=14, fontweight='bold')
ax_pipe.axis('off')

# Subplot 2: Diameter vs Economics U-Curve
ax_cost = plt.subplot(1, 2, 2)
ax_cost.set_title('Financial Feasibility Trade-off upon Pipe Expansion', fontsize=14, fontweight='bold')
ax_cost.set_xlabel('Pipe Inner Diameter D (m)')
ax_cost.set_ylabel('Relative Cost Metric')
ax_cost.grid(True, linestyle='--', alpha=0.6)

# UI Sliders Axes
ax_v = plt.axes([0.15, 0.20, 0.7, 0.03])
ax_mu = plt.axes([0.15, 0.15, 0.7, 0.03])
ax_d = plt.axes([0.15, 0.10, 0.7, 0.03])

# Init Values
s_v = Slider(ax_v, 'Target Velocity (m/s)', 0.5, 5.0, valinit=2.0)
s_mu = Slider(ax_mu, 'Abs Viscosity (Pa.s)', 0.001, 0.1, valinit=0.01)
s_d = Slider(ax_d, 'Design Diameter D (m)', 0.02, 0.20, valinit=0.05)

# Constants
L = 100.0
k1 = 0.02 # Pumping electric coefficient
k2 = 1.0e6 # Pipe infrastructure material coefficient

# Drawing objects
d_init = s_d.val
pipe_outer = patches.Circle((0,0), radius=d_init/2, fill=False, color='black', lw=6)
ax_pipe.add_patch(pipe_outer)
fluid_inner = patches.Circle((0,0), radius=d_init/2 - 0.003, fill=True, color='skyblue', alpha=0.7)
ax_pipe.add_patch(fluid_inner)

friction_arrows = []
for _ in range(8):
    arrow = ax_pipe.annotate('', xy=(0,0), xytext=(0,0), arrowprops=dict(facecolor='red', edgecolor='red', width=3, headwidth=10))
    friction_arrows.append(arrow)

D_arr = np.linspace(0.02, 0.20, 100)
line_pump, = ax_cost.plot([], [], 'b--', label='Pump Op Cost (Friction Base)')
line_pipe, = ax_cost.plot([], [], 'g-.', label='Initial Pipe Infra Cost')
line_total, = ax_cost.plot([], [], 'k-', lw=2, label='Total Merged Cost')
pt_current, = ax_cost.plot([], [], 'ro', markersize=10, label='Current Tuned Diameter')
opt_line = ax_cost.axvline(x=0.05, color='red', linestyle=':', alpha=0.7)

ax_cost.legend(loc='upper right')
ax_cost.set_xlim(0.02, 0.20)
ax_cost.set_ylim(0, 50000)

text_status = fig.text(0.5, 0.01, '', ha='center', fontsize=12, fontweight='bold', color='indigo')

def update(val=None):
    v = s_v.val
    mu = s_mu.val
    d_cur = s_d.val
    
    pipe_outer.set_radius(d_cur/2)
    fluid_inner.set_radius(d_cur/2 - 0.003)
    
    # Hagen-Poiseuille
    dP_cur = (32 * mu * L * v) / (d_cur**2)
    max_dP = (32 * mu * L * v) / (0.02**2)
    arrow_scale = np.clip(dP_cur / max_dP * (d_cur/2), 0.005, d_cur/2 - 0.003)
    
    angles = np.linspace(0, 2*np.pi, 8, endpoint=False)
    for i, angle in enumerate(angles):
        x_edge = (d_cur/2) * np.cos(angle)
        y_edge = (d_cur/2) * np.sin(angle)
        x_center = (d_cur/2 - arrow_scale) * np.cos(angle)
        y_center = (d_cur/2 - arrow_scale) * np.sin(angle)
        friction_arrows[i].xytext = (x_edge, y_edge)
        friction_arrows[i].xy = (x_center, y_center)
        
    cost_pump_arr = k1 * (32 * mu * L * v) / (D_arr**2)
    cost_pipe_arr = k2 * (D_arr**2.5) 
    cost_total_arr = cost_pump_arr + cost_pipe_arr
    
    line_pump.set_data(D_arr, cost_pump_arr)
    line_pipe.set_data(D_arr, cost_pipe_arr)
    line_total.set_data(D_arr, cost_total_arr)
    
    c_pump = k1 * (32 * mu * L * v) / (d_cur**2)
    c_pipe = k2 * (d_cur**2.5)
    pt_current.set_data([d_cur], [c_pump + c_pipe])
    
    min_idx = np.argmin(cost_total_arr)
    opt_d = D_arr[min_idx]
    opt_line.set_xdata([opt_d, opt_d])
    ax_cost.set_ylim(0, np.percentile(cost_total_arr, 95) * 1.3)
    
    msg = (f"[Real-time] ID: {d_cur:.3f} m ➔ Friction ΔP: {dP_cur:,.0f} Pa\n"
           f"💡 [Optimum Target] Total Cost Minimum Valley: {opt_d:.3f} m\n"
           f"▶ Topic 2 Answer: Expanding pipes indefinitely to save pump energy results in a catastrophic Spike in initial pipeline facility investments!")
    text_status.set_text(msg)
    fig.canvas.draw_idle()

s_v.on_changed(update)
s_mu.on_changed(update)
s_d.on_changed(update)
update()
plt.show()
