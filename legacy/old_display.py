import socket
import os
import time
import ctypes
HOST, PORT = "10.26.142.14", 80
# HOST, PORT = "localhost", 80
os.system("mode con: cols=70 lines=30")
old_messages = ''
while True:
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
            sock.sendall(bytes(chr(2), "utf-8"))
            count = sock.recv(1024).decode()
            ctypes.windll.kernel32.SetConsoleTitleA(bytes(str(count) + " users online", "utf-8"))
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
