import socket

HOST = "127.0.0.1" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                print(data)
                data = data.decode()    # decode the binary message to string
                data = "Hello from Python socket server: " + data
                data = data.encode()    # encode the string message to binary
                client.sendall(data) # Echo back to client
    except: 
        print("Closing socket")
        client.close()
        s.close()    