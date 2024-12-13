import numpy as np
import matplotlib.pyplot as plt

def simulate_wind_speed(v_char, num_samples):
    return v_char * np.sqrt(-np.log(1 - np.random.rand(num_samples)))

def simulate_monthly_max_wind_speed(v_char, days_per_month, num_simulations):
    return np.array([np.max(simulate_wind_speed(v_char, days_per_month)) for _ in range(num_simulations)])

# Parameters
v_char_rotterdam = 10.67229219
v_char_vienna = 8.542709123
days_per_month = 30
num_simulations = 1000

# Simulate wind speeds
rotterdam_wind = simulate_wind_speed(v_char_rotterdam, num_simulations)
vienna_wind = simulate_wind_speed(v_char_vienna, num_simulations)

# Simulate monthly maximum wind speeds
rotterdam_max = simulate_monthly_max_wind_speed(v_char_rotterdam, days_per_month, num_simulations)
vienna_max = simulate_monthly_max_wind_speed(v_char_vienna, days_per_month, num_simulations)

# Plotting
plt.figure(figsize=(12, 6))
plt.hist(rotterdam_wind, bins=30, alpha=0.5, label='Rotterdam regular wind')
plt.hist(rotterdam_max, bins=30, alpha=0.5, label='Rotterdam monthly maxima')
plt.hist(vienna_wind, bins=30, alpha=0.5, label='Vienna regular wind')
plt.hist(vienna_max, bins=30, alpha=0.5, label='Vienna monthly maxima')
plt.xlabel('Wind speed (m/s)')
plt.ylabel('Frequency')
plt.title('Monte Carlo Simulation of Wind Speeds')
plt.legend()
plt.show()
