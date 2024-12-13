import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set the seed for reproducibility
np.random.seed(42)

# Define the number of days to simulate
num_days = 365

# Define the weather parameters
num_params = 3  # Temperature, Humidity, Wind Speed

# Generate random weather data using Monte Carlo method
weather_data = np.random.rand(num_days, num_params) * [
    30,  # Max temperature (C)
    100,  # Max humidity (%)
    50  # Max wind speed (km/h)
]

# Normalize the data to realistic ranges
weather_data[:, 0] = weather_data[:, 0] * 20 + 10  # Temperature (C) between 10-30
weather_data[:, 1] = weather_data[:, 1] * 80 + 20  # Humidity (%) between 20-100
weather_data[:, 2] = weather_data[:, 2] * 40 + 10  # Wind Speed (km/h) between 10-50

# Create a Pandas DataFrame for easier data manipulation
df = pd.DataFrame(weather_data, columns=['Temperature (C)', 'Humidity (%)', 'Wind Speed (km/h)'])

# Optional: Plot the data
plt.figure(figsize=(12, 6))
plt.subplot(1, 3, 1)
plt.plot(df['Temperature (C)'])
plt.title('Temperature')

plt.subplot(1, 3, 2)
plt.plot(df['Humidity (%)'])
plt.title('Humidity')

plt.subplot(1, 3, 3)
plt.plot(df['Wind Speed (km/h)'])
plt.title('Wind Speed')
plt.tight_layout()
plt.show()

# Print the first few rows of the DataFrame
print(df.head())
