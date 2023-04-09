import json
import logging
import sys
import pandas as pd

import greengrasssdk

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# SDK Client
client = greengrasssdk.client("iot-data")

# Counter
my_counter = 0
def lambda_handler(event, context):
    global my_counter
    global max_co2_emission
    #TODO1: Get your data
    data_folder = "data2"
    vehicle_files = [f"{data_folder}/vehicle{i}.csv" for i in range(0, 4)]
    for file in vehicle_files:
        data = pd.read_csv(file)
        for index, row in data.iterrows():
            co2_emission = row["vehicle_CO2"]

            # Send the CO2 emission data to the cloud
            client.publish(
                topic=f"vehicle_emissions/{file}",
                payload=json.dumps({"vehicle_CO2": co2_emission}),
            )

    #TODO2: Calculate max CO2 emission
    max_co2_emission_topic = "max/co2/emission"
    max_co2_emissions = []

    def on_message_received(topic, payload):
        nonlocal max_co2_emissions
        max_co2_emission = json.loads(payload)["max_vehicle_CO2"]
        max_co2_emissions.append(max_co2_emission)

    # Subscribe to the topic to receive max CO2 emission values
    client.subscribe(
        topic=max_co2_emission_topic,
        callback=on_message_received,
    )


    #TODO3: Return the result
    result = {
        "message": f"Hello world! Sent from Greengrass Core. Invocation Count: {my_counter}",
        "max_CO2_emissions": max_co2_emissions,
    }

    client.publish(
        topic="hello/world/counter",
        payload=json.dumps(result),
    )

    my_counter += 1

    return