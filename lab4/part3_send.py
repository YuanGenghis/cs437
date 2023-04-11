# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import pandas as pd
import numpy as np


#TODO 1: modify the following parameters
#Starting and end index, modify this
device_st = 0
device_end = 5

#Path to the dataset, modify this
data_path = "data2/vehicle{}.csv"

#Path to your certificates, modify this
certificate_formatter = "./aws/ec2_cert/{}-certificate.pem.crt"
key_formatter = "./aws/ec2_cert/{}-private.pem.key"

device_identifiers = [
    "418dbfbb2676ef8e6a4181c0b2130ecfb12fe3be54c60580181920186230daa0"
]

csv_input = pd.read_csv('./data2/vehicle0.csv')
csv_input['vehicle_id'] = 1
csv_input.to_csv('./data2/vehicle0_updated.csv', index=False)

data_csv = pd.read_csv (r'./data2/vehicle0_updated.csv')
data_csv.to_json (r'./data2/vehicle0.json')
data_json = pd.read_json(r'./data2/vehicle0.json')
data_json = data_json[['vehicle_CO2','vehicle_CO', 'vehicle_HC', 'vehicle_id']]
data_json_vehicle0 = json.loads(data_json.to_json(orient='records'))


csv_input_1 = pd.read_csv('./data2/vehicle1.csv')
csv_input_1['vehicle_id'] = 2
csv_input_1.to_csv('./data2/vehicle1_updated.csv', index=False)

data_csv_1 = pd.read_csv (r'./data2/vehicle1_updated.csv')
data_csv_1.to_json (r'./data2/vehicle1.json')
data_json_1 = pd.read_json(r'./data2/vehicle1.json')
data_json_1 = data_json_1[['vehicle_CO2','vehicle_CO', 'vehicle_HC', 'vehicle_id']]
data_json_vehicle1 = json.loads(data_json_1.to_json(orient='records'))

csv_input_2 = pd.read_csv('./data2/vehicle2.csv')
csv_input_2['vehicle_id'] = 3
csv_input_2.to_csv('./data2/vehicle2_updated.csv', index=False)

data_csv_2 = pd.read_csv (r'./data2/vehicle2_updated.csv')
data_csv_2.to_json (r'./data2/vehicle2.json')
data_json_2 = pd.read_json(r'./data2/vehicle2.json')
data_json_2 = data_json_2[['vehicle_CO2','vehicle_CO', 'vehicle_HC', 'vehicle_id']]
data_json_vehicle2 = json.loads(data_json_2.to_json(orient='records'))


csv_input_3 = pd.read_csv('./data2/vehicle3.csv')
csv_input_3['vehicle_id'] = 4
csv_input_3.to_csv('./data2/vehicle3_updated.csv', index=False)

data_csv_3 = pd.read_csv (r'./data2/vehicle3_updated.csv')
data_csv_3.to_json (r'./data2/vehicle3.json')
data_json_3 = pd.read_json(r'./data2/vehicle3.json')
data_json_3 = data_json_3[['vehicle_CO2','vehicle_CO', 'vehicle_HC', 'vehicle_id']]
data_json_vehicle3 = json.loads(data_json_3.to_json(orient='records'))

csv_input_4 = pd.read_csv('./data2/vehicle4.csv')
csv_input_4['vehicle_id'] = 5
csv_input_4.to_csv('./data2/vehicle4_updated.csv', index=False)

data_csv_4 = pd.read_csv (r'./data2/vehicle4_updated.csv')
data_csv_4.to_json (r'./data2/vehicle4.json')
data_json_4 = pd.read_json(r'./data2/vehicle4.json')
data_json_4 = data_json_4[['vehicle_CO2','vehicle_CO', 'vehicle_HC', 'vehicle_id']]
data_json_vehicle4 = json.loads(data_json_4.to_json(orient='records'))



class MQTTClient:
    def __init__(self, device_id, cert, key):
        # For certificate based connection
        self.device_id = str(device_id)
        self.state = 0
        self.client = AWSIoTMQTTClient(self.device_id)
        #TODO 2: modify your broker address
        self.client.configureEndpoint("ark93xc36vml4-ats.iot.us-east-2.amazonaws.com", 8883)
        self.client.configureCredentials("./aws/ec2_cert/AmazonRootCA1.pem", key, cert)
        self.client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.client.configureMQTTOperationTimeout(5)  # 5 sec
        self.client.onMessage = self.customOnMessage
        

    def customOnMessage(self,message):
        #TODO3: fill in the function to show your received message
        payload_str = message.payload.decode('utf-8')
        print("client {} received payload {} from topic {}".format(self.device_id, payload_str, message.topic))


    # Suback callback
    def customSubackCallback(self,mid, data):
        #You don't need to write anything here
        pass


    # Puback callback
    def customPubackCallback(self,mid):
        #You don't need to write anything here
        pass


    def publish(self, Payload="payload"):

        # Subscribe to the topic
        self.client.subscribeAsync("max/co2/4", 1, ackCallback=self.customSubackCallback)

        # send vehivle 0 data
        # for obj in data_json_vehicle0:
        #     # Publish the JSON-formatted message
        #     self.client.publishAsync("co2/emission", json.dumps(obj), 1, ackCallback=self.customPubackCallback)

        # send vehivle 1 data
        # for obj in data_json_vehicle1:
        #     # Publish the JSON-formatted message
        #     self.client.publishAsync("co2/emission", json.dumps(obj), 1, ackCallback=self.customPubackCallback)

        # # send vehivle 2 data
        # for obj in data_json_vehicle2:
        #     # Publish the JSON-formatted message
        #     self.client.publishAsync("co2/emission", json.dumps(obj), 1, ackCallback=self.customPubackCallback)

        # # send vehivle 3 data
        # for obj in data_json_vehicle3:
        #     # Publish the JSON-formatted message
        #     self.client.publishAsync("co2/emission", json.dumps(obj), 1, ackCallback=self.customPubackCallback)

        # send vehivle 4 data
        for obj in data_json_vehicle4:
            # Publish the JSON-formatted message
            self.client.publishAsync("max/co2/4", json.dumps(obj), 1, ackCallback=self.customPubackCallback)

        print('Published')



print("Loading vehicle data...")
data = []
for i in range(5):
    a = pd.read_csv(data_path.format(i))
    data.append(a)

print("Initializing MQTTClients...")
clients = []
for device_id in range(device_st, device_end):
    client = MQTTClient(device_id,certificate_formatter.format(device_identifiers[0],device_identifiers[0]) ,key_formatter.format(device_identifiers[0],device_identifiers[0]))
    client.client.connect()
    clients.append(client)
 

while True:
    print("send now?")
    x = input()
    if x == "s":
        for i,c in enumerate(clients):
            c.publish()

    elif x == "d":
        for c in clients:
            c.client.disconnect()
        print("All devices disconnected")
        exit()
    else:
        print("wrong key pressed")

    time.sleep(10)





