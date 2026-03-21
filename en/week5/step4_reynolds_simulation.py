"""
Week 5 Lab: Step 4 - Reynolds Number Flow Regimes Particle Animation Simulator
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# Font Config (Using Arial/San-serif for English)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

# Fixed Parameter: Density of Clear Apple Juice Concentrate
rho = 1050  # kg/m^3

fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(bottom=0.35, top=0.82)

ax.set_xlim(0, 10)
ax.set_ylim(-1.5, 1.5)
ax.set_title('Flow Regime Simulation (Laminar vs Turbulent)', fontsize=16, fontweight='bold', pad=35)
ax.set_yticks([])
ax.set_xticks([])

# Pipe Boundary Lines
ax.axhline(1, color='black', lw=6)
ax.axhline(-1, color='black', lw=6)
ax.fill_between([0, 10], 1, 1.1, color='gray', alpha=0.5)
ax.fill_between([0, 10], -1.1, -1, color='gray', alpha=0.5)

# Initialize Particles
num_particles = 400
x = np.random.uniform(0, 10, num_particles)
y = np.random.uniform(-0.95, 0.95, num_particles)

scatter = ax.scatter(x, y, s=15, c='blue', alpha=0.6)

# UI Sliders Axes
ax_v = plt.axes([0.15, 0.20, 0.7, 0.03])
ax_d = plt.axes([0.15, 0.15, 0.7, 0.03])
ax_mu = plt.axes([0.15, 0.10, 0.7, 0.03])

# Create Sliders (Init near Transition Zone)
s_v = Slider(ax_v, 'Velocity $v$ (m/s)', 0.1, 5.0, valinit=1.5)
s_d = Slider(ax_d, 'Pipe Inner Dia $D$ (m)', 0.01, 0.2, valinit=0.05)
s_mu = Slider(ax_mu, r'Viscosity $\mu$ (Pa.s)', 0.001, 0.1, valinit=0.03)

# Status Text Overlay
text_re = ax.text(0.5, 1.05, '', transform=ax.transAxes, ha='center', fontsize=15, fontweight='bold')
text_desc = ax.text(0.5, -0.1, '', transform=ax.transAxes, ha='center', fontsize=12, color='dimgray')

def update_text(val):
    v = s_v.val
    d = s_d.val
    mu = s_mu.val
    Re = (rho * v * d) / mu
    
    if Re < 2100:
        state = "Laminar Flow"
        color = "blue"
        desc = "Fluids travel smoothly in parallel layers. Pumping costs drop, but Heat Exchange mixing efficiency is extremely poor."
    elif Re < 4000:
        state = "Transition Zone"
        color = "purple"
        desc = "Unstable region indicating the sudden breakdown of laminar boundary layers."
    else:
        state = "Turbulent Flow"
        color = "red"
        desc = "Violent vortices explode! Friction pressure leaps aggressively, but Pasteurization/Heat Exchange efficiency skyrockets!"
        
    text_re.set_text(f"Reynolds No (Re): {Re:,.0f} -> {state}")
    text_re.set_color(color)
    text_desc.set_text(desc)

# Connect UI interactions
s_v.on_changed(update_text)
s_d.on_changed(update_text)
s_mu.on_changed(update_text)

def animate(frame):
    v_avg = s_v.val
    d = s_d.val
    mu = s_mu.val
    Re = (rho * v_avg * d) / mu
    
    global x, y
    
    if Re < 2100:
        # Laminar: Parabolic velocity profile, zero noise
        v_local = 2 * v_avg * (1 - y**2)
        dy = 0
    elif Re < 4000:
        # Transition: Slight structural disruption
        v_local = v_avg * (1 - y**2)**0.5
        dy = np.random.normal(0, 0.03 * v_avg, num_particles)
    else:
        # Turbulent: Chaotic vortex dynamics
        v_local = v_avg * np.ones_like(y)
        dy = np.random.normal(0, 0.25 * v_avg, num_particles)
        
    # Scale adjustment for visual appeal inside the plot constraints
    dx = v_local * 0.1
    
    x += dx
    y += dy
    
    # Bounce physics at pipe boundary
    y = np.clip(y, -0.96, 0.96)
    
    # Respawn particles exiting the pipeline
    out_of_bounds = x > 10
    x[out_of_bounds] = 0
    y[out_of_bounds] = np.random.uniform(-0.95, 0.95, np.sum(out_of_bounds))
    
    # Dynamic coloring based on Re magnitude
    if Re < 2100:
        scatter.set_color('blue')
    elif Re < 4000:
        scatter.set_color('purple')
    else:
        scatter.set_color('red')
        
    scatter.set_offsets(np.c_[x, y])
    return scatter,

ani = FuncAnimation(fig, animate, frames=200, interval=50, blit=False)

update_text(0)
plt.show()
