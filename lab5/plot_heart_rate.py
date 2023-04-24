import json
import numpy as np
import matplotlib.pyplot as plt


# Load the data as a Python dictionary
with open('zebra_data.json', 'r') as file:
    data = json.load(file)

color_list = ['blue', 'green', 'red', 'cyan', 'm', "yellow", "black", "orange", "purple"]

# Extract oxygen saturation and heart rate data for each zebra
for idx, (zebra_id, zebra_data) in enumerate(data.items()):
    timestamps = sorted(map(float, zebra_data.keys()))
    heart_rates = [zebra_data[f"{t:.2f}"]['heart_rate'] for t in timestamps if f"{t:.2f}" in zebra_data]

    plt.scatter(timestamps, heart_rates, color=color_list[idx % len(color_list)], label=f"Zebra {zebra_id}")

plt.xlabel('Timestamps')
plt.ylabel('Heart Rate')
plt.title('Heart Rate of Zebras Over Time')
plt.legend()
plt.grid()
plt.show()





