import json
import numpy as np
import matplotlib.pyplot as plt


# Load the data as a Python dictionary
with open('zebra_data.json', 'r') as file:
    data = json.load(file)

marker_list = ['o', 's', '^', 'd', 'v', ">", "1", "2", "3"]
color_list = ['blue', 'green', 'red', 'cyan', 'm', "yellow", "black", "orange", "purple"]

# Plot the temperature for each zebra
for idx, (zebra_id, zebra_data) in enumerate(data.items()):
    timestamps = sorted(map(float, zebra_data.keys()))
    temperatures = [zebra_data[f"{t:.2f}"]['temperature'] for t in timestamps if f"{t:.2f}" in zebra_data]

    plt.plot(timestamps, temperatures, marker=marker_list[idx % len(marker_list)], linestyle='-', color=color_list[idx % len(color_list)], label=f"Zebra {zebra_id}")

plt.xlabel('Timestamp')
plt.ylabel('Temperature')
plt.title('Temperature of Zebras Over Time')
plt.legend()
plt.grid()
plt.show()