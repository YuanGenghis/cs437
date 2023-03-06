import socket
import threading
import picar_4wd as fc
import time
import psutil

HOST = "192.168.10.35" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

valid_commands = [
    'FORWARD',
    'BACKWARD',
    'LEFT',
    'RIGHT',
    'STOP'
]

class car_commander(object):
    def __init__(self) -> None:
        self.command = 'STOP'
        self.speed = 0
        self.command_lock = threading.Lock()
      
    def get_speed(self):
        return self.speed

    def get_current_move_command(self):
        with self.command_lock:
            ret = self.command
        return ret
    
    def set_current_move_command(self, command):
        self.command = command
        self.speed = 20
        if self.command == 'FORWARD':
            fc.forward(self.speed)
        elif self.command == 'BACKWARD':
            fc.backward(self.speed)
        elif self.command == 'RIGHT':
            fc.turn_right(self.speed)
        elif self.command == 'LEFT':
            fc.turn_left(self.speed)
        elif self.command == 'STOP':
            self.speed = 0
            fc.stop()
        else:
            self.speed = 0
            fc.stop()
        
            

my_car = car_commander()

def get_current_move_command():
    return my_car.get_current_move_command()

def get_current_speed():
    return my_car.get_speed() # TODO: implement this!

def get_temperature():
    temp_val = psutil.sensors_temperatures()['cpu_thermal'][0].current
    print(temp_val)

    return temp_val # TODO: implement this!

def process_package(data):
    data = data.decode().strip()   # decode the binary message to string
    if data in valid_commands:
        my_car.set_current_move_command(data)
    else:
        print("Invalid command received!: {}".format(data))
        return

def generate_return_package():
    ret_str = '{},{},{}'.format(
        get_current_move_command(),
        get_current_speed(),
        get_temperature()
    )
    return ret_str.encode() # encode the string to binary format

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                # print("Received data:")
                # print(data)
                process_package(data)
                ret_packet = generate_return_package()
                print("Sending data:")
                print(ret_packet)
                client.sendall(ret_packet)
    except E:
        print(E) 
        print("Closing socket")
        client.close()
        s.close()    
