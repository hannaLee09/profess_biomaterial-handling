import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Matplotlib Font Setting
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False 

print("==================================================")
print(" 🍏 Week 5 Lab Step 2: Interactive Real-time Simulator ")
print("==================================================\n")
print("Tweak the UI sliders at the bottom to dynamically observe the optimal friction parameters!")

# 1. Simulation variables and fixed constants initialization
R_const = 8.314
pipe_L_init = 100.0
pump_efficiency = 0.7
run_hours = 1000
init_temp = 10.0
heat_cp = 4.18
temps_C = np.arange(10, 81, 1)
temps_K = temps_C + 273.15

# Initial Slider Values
pipe_D_init = 0.05
velocity_init = 2.0
mu_0_init = 0.0001
E_a_init = 18000
elec_cost_kw_init = 120
heat_cost_kw_init = 40

# 2. Viscosity constraint & Cost computation logic integration
def calc_costs(pipe_D, velocity, mu_0, E_a, elec_cost, heat_cost):
    # Arrhenius and Hagen-Poiseuille integration
    viscosity = mu_0 * np.exp(E_a / (R_const * temps_K))
    delta_P = (32 * viscosity * pipe_L_init * velocity) / (pipe_D ** 2)
    vol_flow = (np.pi * (pipe_D / 2) ** 2) * velocity
    
    pump_power_W = (vol_flow * delta_P) / pump_efficiency
    cost_pump = (pump_power_W / 1000) * run_hours * elec_cost
    
    heat_rate = vol_flow * 1000
    heat_kw = heat_rate * heat_cp * (temps_C - init_temp)
    cost_heat = heat_kw * run_hours * heat_cost
    
    cost_total = cost_pump + cost_heat
    return cost_pump, cost_heat, cost_total

# 3. Main Figure Plot Configuration
fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(bottom=0.5) # Expand bottom margin adequately to accommodate sliders

# Compute initial visualization plot
cp_init, ch_init, ct_init = calc_costs(pipe_D_init, velocity_init, mu_0_init, E_a_init, elec_cost_kw_init, heat_cost_kw_init)

l_pump, = ax.plot(temps_C, cp_init, label='Motor Pumping Cost', linestyle='--', color='blue', alpha=0.7)
l_heat, = ax.plot(temps_C, ch_init, label='Boiler Preheating Cost', linestyle='-.', color='orange', alpha=0.7)
l_total, = ax.plot(temps_C, ct_init, label='Total Energy Cost', linewidth=2.5, color='green')

opt_idx = np.argmin(ct_init)
opt_temp = temps_C[opt_idx]
opt_line = ax.axvline(x=opt_temp, color='red', alpha=0.5, label=f'Optimal Transport Temp: {opt_temp}℃')

ax.set_title('Interactive Parameter-based Trade-off Margin Analysis', fontsize=14, fontweight='bold')
ax.set_xlabel('Pipeline Transport Temperature (℃)', fontsize=12)
ax.set_ylabel('Annual Total Energy Operational Cost (KRW)', fontsize=12)
ax.legend(loc='upper right', fontsize=10)
ax.grid(True, linestyle=':', alpha=0.7)

# 4. Render Interface Sliders iteratively
axcolor = 'whitesmoke'
ax_D  = plt.axes([0.20, 0.40, 0.65, 0.03], facecolor=axcolor)
ax_v  = plt.axes([0.20, 0.35, 0.65, 0.03], facecolor=axcolor)
ax_mu = plt.axes([0.20, 0.30, 0.65, 0.03], facecolor=axcolor)
ax_Ea = plt.axes([0.20, 0.25, 0.65, 0.03], facecolor=axcolor)
ax_el = plt.axes([0.20, 0.20, 0.65, 0.03], facecolor=axcolor)
ax_ht = plt.axes([0.20, 0.15, 0.65, 0.03], facecolor=axcolor)

s_D  = Slider(ax_D,  'Inner Diameter(m)', 0.01, 0.20, valinit=pipe_D_init, valstep=0.01)
s_v  = Slider(ax_v,  'Target Velocity(m/s)', 0.5, 10.0, valinit=velocity_init, valstep=0.1)
s_mu = Slider(ax_mu, 'Init Viscosity(mu_0)', 0.00001, 0.002, valinit=mu_0_init, valfmt='%1.5f')
s_Ea = Slider(ax_Ea, 'Activation Energy', 10000, 30000, valinit=E_a_init, valstep=500)
s_el = Slider(ax_el, 'Elec. Unit(KRW/kWh)', 50, 300, valinit=elec_cost_kw_init, valstep=10)
s_ht = Slider(ax_ht, 'Heat Unit(KRW/MJ)', 10, 150, valinit=heat_cost_kw_init, valstep=5)

# 5. Establish Update Callback Framework upon Slider Event Trigger
def update(val):
    # Reroute calculation flow utilizing dynamic inputs
    cp, ch, ct = calc_costs(s_D.val, s_v.val, s_mu.val, s_Ea.val, s_el.val, s_ht.val)
    
    # Reload line attributes
    l_pump.set_ydata(cp)
    l_heat.set_ydata(ch)
    l_total.set_ydata(ct)
    
    # Re-scale constraints actively
    ax.relim()
    ax.autoscale_view()
    
    # Revamp Optimal indicator point
    idx = np.argmin(ct)
    new_opt_temp = temps_C[idx]
    opt_line.set_xdata([new_opt_temp, new_opt_temp])
    opt_line.set_label(f'Optimal Transport Temp: {new_opt_temp}℃')
    
    ax.legend(loc='upper right')
    fig.canvas.draw_idle()

# Bind triggers
s_D.on_changed(update)
s_v.on_changed(update)
s_mu.on_changed(update)
s_Ea.on_changed(update)
s_el.on_changed(update)
s_ht.on_changed(update)

# Emit visuals via display
plt.show()
