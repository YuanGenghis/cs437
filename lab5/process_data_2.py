from collections import defaultdict
import json

filename = "./dataset/my_data.txt"

data = open(filename, "r").read()

def parse_data(data):
    zebras = set()
    records = []
    current_record = {}
    
    for line in data.strip().split("\n"):
        if "Zebra" in line:
            zebras.add(line.split(":")[1])
        if "Timestamp" in line:
            if current_record:
                records.append(current_record)
                current_record = {}
            current_record["timestamp"] = float(line.split(": ")[1])
        elif ":" in line:
            parts = line.strip().split(": ")
            if len(parts) == 2:
                key, value = parts
                if "[" in value:
                    value = list(map(float, value.strip("[]").split(",")))
                else:
                    value = float(value)
                current_record[key] = value

    records.append(current_record)  # Append the last record
    print(zebras)
    return records

parsed_data = parse_data(data)

with open("output.json", "w") as outfile:
    json.dump(parsed_data, outfile, indent=4)

print("Data saved to output.json")