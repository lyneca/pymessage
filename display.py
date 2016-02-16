import socket
import os
import time
HOST, PORT = "10.26.142.14", 80
# HOST, PORT = "localhost", 80
old_messages = ''
while True:
    while True:
        try:
            sock = socket.socket()
            sock.connect((HOST, PORT))
            break
        except (ConnectionRefusedError, ConnectionResetError):
            print("Can't connect to server.")
            time.sleep(1)
    sock.sendall(bytes(chr(1), "utf-8"))
    messages = str(sock.recv(4096), "utf-8")
    if not messages == old_messages:
        os.system('cls')
        print(messages)
        old_messages = messages
    time.sleep(0.1)
