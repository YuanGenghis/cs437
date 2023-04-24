import json
import numpy as np
import matplotlib.pyplot as plt


# Load the data as a Python dictionary
with open('zebra_data.json', 'r') as file:
    data = json.load(file)

# def calculate_speed(location1, location2, time1, time2):
#     distance = np.sqrt((location2[0] - location1[0])**2 + (location2[1] - location1[1])**2)
#     time_diff = time2 - time1
#     return distance / time_diff

# speeds = []
# timestamps_all = []

# # Calculate the movement speed for each zebra
# for zebra_id, zebra_data in data.items():
#     timestamps = sorted(map(float, zebra_data.keys()))
#     locations = [zebra_data[f"{t:.2f}"]['location'] for t in timestamps if f"{t:.2f}" in zebra_data]

#     for i in range(1, len(timestamps)):
#         speed = calculate_speed(locations[i-1], locations[i], timestamps[i-1], timestamps[i])
#         speeds.append(speed)
#         timestamps_all.append(timestamps[i])

#     # # Calculate the CDF of the movement speed
#     # speeds = np.array(speeds)
#     # sorted_speeds = np.sort(speeds)
#     # cdf = np.linspace(0, 1, len(speeds))

#     # Plot the CDF
#     plt.plot(timestamps_all, speeds, marker='o', linestyle='-')
#     plt.xlabel('Timestamp')
#     plt.ylabel('Movement Speed')
#     plt.title('Movement Speed of Zebras ' + zebra_id)
#     plt.grid()
#     plt.show()


def calculate_speed(location1, location2, time1, time2):
    distance = np.sqrt((location2[0] - location1[0])**2 + (location2[1] - location1[1])**2)
    time_diff = time2 - time1
    return distance / time_diff

marker_list = ['o', 's', '^', 'd', 'v', ">", "1", "2", "3"]
color_list = ['blue', 'green', 'red', 'cyan', 'm', "yellow", "black", "orange", "purple"]

# Calculate the movement speed for each zebra and plot separately
for idx, (zebra_id, zebra_data) in enumerate(data.items()):
    timestamps = sorted(map(float, zebra_data.keys()))
    locations = [zebra_data[f"{t:.2f}"]['location'] for t in timestamps if f"{t:.2f}" in zebra_data]

    timestamps_plot = []
    speeds = []

    for i in range(1, len(timestamps)):
        speed = calculate_speed(locations[i-1], locations[i], timestamps[i-1], timestamps[i])
        speeds.append(speed)
        timestamps_plot.append(timestamps[i])


    plt.plot(timestamps_plot, speeds, marker=marker_list[idx % len(marker_list)], linestyle='-', color=color_list[idx % len(color_list)], label=f"Zebra {zebra_id}")

plt.xlabel('Timestamp')
plt.ylabel('Movement Speed')
plt.title('Movement Speed of Zebras Over Time')
plt.legend()
plt.grid()
plt.show()
#save the plot as a png file
# plt.savefig('plot_speed.png')