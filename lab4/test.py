import json

# Read the JSON file
with open('vehicle1.json', 'r') as f:
    data = json.load(f)

# Loop through the JSON objects and add the row
for obj in data:
    obj['vehicle_id'] = 1
    del obj['timestep_time']
    del obj['vehicle_NOx']
    del obj['vehicle_PMx']
    del obj['vehicle_angle']
    del obj['vehicle_eclass']
    del obj['vehicle_electricity']
    del obj['vehicle_fuel']
    del obj['vehicle_lane']
    del obj['vehicle_noise']
    del obj['vehicle_pos']
    del obj['vehicle_route']
    del obj['vehicle_speed']
    del obj['vehicle_type']
    del obj['vehicle_waiting']
    del obj['vehicle_x']
    del obj['vehicle_y']

# Save the modified JSON file
with open('modified_file2.json', 'w') as f:
    json.dump(data, f)