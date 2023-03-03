import socket

HOST = "127.0.0.1" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

def generate_return_package():
    ret_str = b'123,456'
    return ret_str

def process_package(data):
    data = data.decode()   # decode the binary message to string
    # TODO: implement logic to control the car

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                print("Received data:")
                print(data)
                process_package(data)
                ret_packet = generate_return_package()
                client.sendall(ret_packet)
    except: 
        print("Closing socket")
        client.close()
        s.close()    