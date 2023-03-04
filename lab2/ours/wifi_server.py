import socket
import threading

HOST = "127.0.0.1" # IP address of your Raspberry PI
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
        self.command_lock = threading.Lock()

    def get_current_move_command(self):
        with self.command_lock:
            ret = self.command
        return ret
    
    def set_current_move_command(self, command):
        assert command in valid_commands
        with self.command_lock:
            self.command = command

my_car = car_commander()

def get_current_move_command():
    return my_car.get_current_move_command()

def get_current_speed():
    return 123 # TODO: implement this!

def get_temperature():
    return 123 # TODO: implement this!

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
    except: 
        print("Closing socket")
        client.close()
        s.close()    