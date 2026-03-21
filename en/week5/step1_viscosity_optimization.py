import numpy as np
import matplotlib.pyplot as plt

# Matplotlib Font Setting
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False 

print("==================================================")
print(" 🍏 Week 5 Lab: Clear Apple Juice Pipeline Simulator ")
print("==================================================\n")

# [Part 1] Temperature-Viscosity Data Array Construction
# 1. Temperature range setup: 10 to 80 degrees (1-degree increments)
temps_C = np.arange(10, 81, 1)

# 2. Convert Celsius to Kelvin (Absolute Temperature)
temps_K = temps_C + 273.15

# 3. Universal gas constant and Arrhenius model parameters
R_const = 8.314  # Universal gas constant
mu_0 = 0.0001    # Base viscosity constant
E_a = 18000      # Activation energy

# 4. Viscosity array calculation via Arrhenius equation
viscosity_array = mu_0 * np.exp(E_a / (R_const * temps_K))

print("[STEP 1] Arrhenius viscosity computation complete")
print(f" -> Viscosity at 10°C: {viscosity_array[0]:.5f} Pa·s")
print(f" -> Viscosity at 80°C: {viscosity_array[-1]:.5f} Pa·s\n")

# [Part 2] Pipe Friction Margin Calculation Logic
# 1. Pipe geometry constants and target flow velocity
pipe_L = 100.0   # Pipe length (m)
pipe_D = 0.05    # Pipe inner diameter (m)
velocity = 2.0   # Fluid velocity (m/s)

# 2. Pressure Drop array calculation (Hagen-Poiseuille)
delta_P_array = (32 * viscosity_array * pipe_L * velocity) / (pipe_D ** 2)

# 3. Volumetric Flow Rate and Motor Efficiency
pump_efficiency = 0.7  # Pump efficiency (70%)
vol_flow = (np.pi * (pipe_D / 2) ** 2) * velocity

print("[STEP 2] Pipeline flow resistance and pressure drop calculation complete")
print(f" -> Volumetric flow: {vol_flow:.5f} m^3/s")
print(f" -> Pressure friction drop across 100m at 10°C: {delta_P_array[0]:.2f} Pa\n")

# [Part 3] Pumping Power vs. Heating Power Cost Balance Simulation
# 1. Pump power consumption (W) and annual cost conversion
pump_power_W = (vol_flow * delta_P_array) / pump_efficiency
run_hours = 1000        # Annual operational hours (1000 hours)
elec_cost_kw = 120      # Electricity unit cost (KRW/kWh)

cost_pump_array = (pump_power_W / 1000) * run_hours * elec_cost_kw

# 2. Boiler heating energy logic to reach target temperatures
init_temp = 10.0        # Initial ambient temperature (10°C)
heat_cp = 4.18          # Specific heat approximation for apple juice (kJ/kg·K)
heat_rate = vol_flow * 1000  # Mass flow assuming water density (kg/s)

# 3. Heating cost array computation
# heat_kw_array is calculated in kJ/s, equating to kW
heat_kw_array = heat_rate * heat_cp * (temps_C - init_temp) 
heat_cost_kw = 40       # Heating (steam) unit cost (KRW/MJ)

cost_heat_array = heat_kw_array * run_hours * heat_cost_kw

# 4. Final total integrated cost (Logistics + Preheating)
cost_total_array = cost_pump_array + cost_heat_array

print("[STEP 3] Energy Trade-off cost computation complete\n")

# [Part 4] UI Visual Data Rendering and Optimal Analysis
# 1. Identify the minimum total cost and optimal temperature using np.argmin()
min_idx = np.argmin(cost_total_array)
optimal_temp = temps_C[min_idx]

print("==================================================")
print(f" 🎯 Simulation Result: The lowest energy cost temperature is [{optimal_temp}℃].")
print("==================================================\n")

# 2. Output multi-subplot infographic (1x2 layout)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# [Subplot 1] Viscosity and Pressure Drop Curve (Dual Y-axis)
color1 = '#0056b3'
ax1.set_xlabel('Transport Temperature (℃)', fontsize=12)
ax1.set_ylabel('Absolute Viscosity (Pa·s)', color=color1, fontsize=12)
ax1.plot(temps_C, viscosity_array, color=color1, linewidth=2, label='Viscosity Curve')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.grid(True, linestyle=':', alpha=0.5)

ax1_twin = ax1.twinx()  # Twin Y-axis
color2 = '#d9534f'
ax1_twin.set_ylabel('Pipe Friction Pressure Drop (Pa)', color=color2, fontsize=12)
ax1_twin.plot(temps_C, delta_P_array, color=color2, linestyle='--', linewidth=2, label='Pressure Drop Curve')
ax1_twin.tick_params(axis='y', labelcolor=color2)

ax1.set_title('Viscosity & Friction Resistance Decay vs. Temperature', fontsize=12, fontweight='bold')
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax1_twin.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right', fontsize=10)

# [Subplot 2] Energy Cost Trade-off Margin Analysis
ax2.plot(temps_C, cost_pump_array, label='Motor Pumping Cost', linestyle='--', color='blue', alpha=0.7)
ax2.plot(temps_C, cost_heat_array, label='Boiler Preheating Cost', linestyle='-.', color='orange', alpha=0.7)
ax2.plot(temps_C, cost_total_array, label='Total Energy Cost', linewidth=2.5, color='green')

# Add vertical guideline and point marker indicating optimal temperature
ax2.axvline(x=optimal_temp, color='red', alpha=0.5, label=f'Optimal Transport Temp: {optimal_temp}℃')
ax2.plot(optimal_temp, cost_total_array[min_idx], 'ro', markersize=8) # Lowest point marker

ax2.set_title('Pumping-Heating Dual Cost Trade-off Analysis', fontsize=12, fontweight='bold')
ax2.set_xlabel('Transport Temperature (℃)', fontsize=12)
ax2.set_ylabel('Total Energy Unit Cost (KRW)', fontsize=12)
ax2.legend(loc='upper right', fontsize=10)
ax2.grid(True, linestyle=':', alpha=0.7)

# Display plot
plt.tight_layout()
plt.show()
