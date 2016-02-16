import socket
import os
os.system('start python display.py')
messages = ''
HOST, PORT = "10.2.1.24", 80
os.system("mode con: cols=70 lines=5")
while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data = input('> ')
    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data + "\n", "utf-8"))

        # Receive data from the server and shut down
        messages = str(sock.recv(1024), "utf-8")
    finally:
        sock.close()
        os.system('cls')
