import re
import json
import numpy as np
import matplotlib.pyplot as plt

filename = "./dataset/my_data.txt"

def parse_data(filename):
    with open(filename, "r") as file:
        content = file.read()

    zebras = re.findall(r"Zebra:([a-z0-9]+)", content)

    data = {}

    for zebra in zebras:
        data[zebra] = []

    pattern = re.compile(r"Zebra:([a-z0-9]+) LOG(.*?)\n(===============|$)", re.DOTALL)

    for zebra, log, _ in pattern.findall(content):

        print(zebra)

        single_data = {}

        timestamp_pattern = r'-- Timestamp: (\d+\.\d+)'
        temperature_pattern = r'"temperature": (\d+\.\d+)'
        location_pattern = r'"location": \[(-?\d+\.\d+),(-?\d+\.\d+)\]'
        humidity_pattern = r'"humidity": (\d+\.\d+)'
        oxygen_saturation_pattern = r'"oxygen_saturation": (\d+\.\d+)'
        heart_rate_pattern = r'"heart_rate": (\d+)'

        timestamps = re.findall(timestamp_pattern, log)
        temperatures = re.findall(temperature_pattern, log)
        locations = re.findall(location_pattern, log)
        humidities = re.findall(humidity_pattern, log)
        oxygen_saturations = re.findall(oxygen_saturation_pattern, log)
        heart_rates = re.findall(heart_rate_pattern, log)

        min_len = min(len(timestamps), len(temperatures), len(locations), len(humidities), len(oxygen_saturations), len(heart_rates))


        for i, timestamp in enumerate(timestamps):
            if i < min_len:
                single_data[timestamp] = {
                    "temperature": float(temperatures[i]),
                    "location": [float(locations[i][0]), float(locations[i][1])],
                    "humidity": float(humidities[i]),
                    "oxygen_saturation": float(oxygen_saturations[i]),
                    "heart_rate": int(heart_rates[i])
                    }
        
        data[zebra] = single_data
    return data

data = parse_data(filename)

# Save the data to a JSON file
with open("zebra_data.json", "w") as outfile:
    json.dump(data, outfile, indent=4)
