import socket
import unicurses_test
import os

HOST, PORT = "10.26.142.14", 80
# HOST, PORT = "localhost", 80
os.system("mode con: cols=70 lines=5")
err = []
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
sock.sendall(bytes(chr(3), "utf-8"))
while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data = input('> ')
    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data + "\n", "utf-8"))

        # Receive data from the server and shut down
        messages = str(sock.recv(1024))
    except (ConnectionRefusedError, ConnectionResetError):
        err.append("Can't connect.")
    finally:
        sock.close()
        os.system('cls')
        for i in range(len(err)):
            print(err.pop(i))
