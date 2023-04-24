import json
import numpy as np
import matplotlib.pyplot as plt


# Load the data as a Python dictionary
with open('zebra_data.json', 'r') as file:
    data = json.load(file)

color_list = ['blue', 'green', 'red', 'cyan', 'm', "yellow", "black", "orange", "purple"]

timestamps = []
latitudes = []
longitudes = []

for zebra_id, zebra_data in data.items():
    for timestamp, zebra_stats in zebra_data.items():
        timestamps.append(float(timestamp))
        latitudes.append(zebra_stats["location"][0])
        longitudes.append(zebra_stats["location"][1])
        
plt.figure(figsize=(10, 6))

# Scatter plot
plt.scatter(longitudes, latitudes, c=timestamps, cmap='viridis', marker='o', s=50)

# Optional: Line plot (uncomment the following line to use a line plot instead)
# plt.plot(longitudes, latitudes, linestyle='-', marker='o', markersize=5)

plt.colorbar(label='Timestamp')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Zebra Movement')
plt.grid(True)

plt.show()




