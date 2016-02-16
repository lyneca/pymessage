import socket
import socketserver
from datetime import datetime
import os

controls = [
    chr(0),
    chr(1)
]


def get_server_time():
    return ''.join(datetime.now().isoformat().split('T')[1].split('.')[0])


class Message():
    def __init__(self, message, ip, time):
        self.time = time
        self.message = message
        if ip in users:
            self.name = users[ip]
        else:
            self.name = "anon"
        self.ip = ip

    def __str__(self):
        return self.time + ' ' + self.name + ': ' + self.message

    def update(self):
        if self.ip in users:
            self.name = users[self.ip]


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024).strip().decode()
        if data.split()[0] == ':nick':
            users[self.client_address[0]] = ' '.join(data.split()[1:])
        elif data in controls:
            print(get_server_time() + ": control char from " + self.client_address[0])
        else:
            messages.append(Message(data, self.client_address[0], get_server_time()))
            print(get_server_time() + ": message from " + self.client_address[0])
        out = ''
        for message in messages:
            message.update()
            out += str(message) + '\n'
        self.request.sendall(bytes(out, "utf-8"))


messages = []
users = {}

HOST, PORT = "", 80
print("Starting server...")
server = socketserver.TCPServer((HOST, PORT), TCPHandler)

# Activate the server; this will keep running until you
# interrupt the program with Ctrl-C
try:
    server.serve_forever()
except KeyboardInterrupt:
    print("Stopping server...")
    server.shutdown()
    print("Stopped.")
