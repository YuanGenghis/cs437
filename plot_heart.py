import json
import numpy as np
import matplotlib.pyplot as plt


# Load the data as a Python dictionary
with open('zebra_data.json', 'r') as file:
    data = json.load(file)

color_list = ['b', 'g', 'r', 'c', 'm']

# Extract oxygen saturation and heart rate data for each zebra
for idx, (zebra_id, zebra_data) in enumerate(data.items()):
    timestamps = sorted(map(float, zebra_data.keys()))
    oxygen_saturations = [zebra_data[f"{t:.2f}"]['oxygen_saturation'] for t in timestamps if f"{t:.2f}" in zebra_data]
    heart_rates = [zebra_data[f"{t:.2f}"]['heart_rate'] for t in timestamps if f"{t:.2f}" in zebra_data]

    plt.scatter(oxygen_saturations, heart_rates, color=color_list[idx % len(color_list)], label=f"Zebra {zebra_id}")

plt.xlabel('Oxygen Saturation')
plt.ylabel('Heart Rate')
plt.title('Relationship Between Oxygen Saturation and Heart Rate')
plt.legend()
plt.grid()
plt.show()





