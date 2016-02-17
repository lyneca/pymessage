import socketserver
from datetime import datetime

controls = [
    chr(0),
    chr(1)
]

pwd = "kek"

messages = []
users = {}


def get_server_time():
    return ''.join(datetime.now().isoformat().split('T')[1].split('.')[0])


class Message:
    def __init__(self, message, ip, time, datetime, u):
        self.time = time
        self.u = u
        self.datetime = datetime
        self.message = message
        self.ip = ip
        self.is_message = message is not None
        if ip in users:
            self.name = users[self.ip] + ' [' + self.ip + ']'
        else:
            self.name = 'anon [' + self.ip + ']'

    def __str__(self):
        if self.u:
            return self.time + ' ' + self.name + ': ' + self.message
        else:
            return " * " + self.message + " *"

    def update(self):
        if self.ip in users:
            self.name = users[self.ip] + ' [' + self.ip + ']'
        else:
            self.name = 'anon [' + self.ip + ']'


def get_ip_by_user(user):
    for u in users:
        if users[u] == user:
            return u


def get_last_message_by(ip):
    for m in reversed(messages):
        if m.ip == ip:
            return m
    return None


def add_message(ip, msg=None, u=True):
    messages.append(Message(msg, ip, get_server_time(), datetime.now(), u))


def count_online():
    c = 0
    for user in users:
        if not get_last_message_by(user) is None:
            print((datetime.now() - get_last_message_by(user).datetime).total_seconds())
            if (datetime.now() - get_last_message_by(user).datetime).total_seconds() < 1:
                c += 1
    return c


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        out = ''
        send = True
        ip = self.client_address[0]
        data = self.request.recv(1024).decode().strip()
        if data.split()[0] == ':nick':
            if ip in users:
                last_nick = users[ip]
            else:
                last_nick = 'anon [' + ip + ']'
            users[ip] = ' '.join(data.split()[1:])
            add_message(ip, last_nick + " is now known as " + data.split()[1], False)
        elif data.split()[0] == ':ping':
            if not get_last_message_by(get_ip_by_user(data.split()[1])) is None:
                if (datetime.now() - get_last_message_by(get_ip_by_user(data.split()[1])).datetime).total_seconds() < 1:
                    add_message(ip, users[ip] + " pinged " + data.split()[1] + ": online in past second", False)
                else:
                    add_message(ip, users[ip] + " pinged " + data.split()[1] + ": not online in past second", False)
            else:
                add_message(ip, users[ip] + " pinged " + data.split()[1] + ": not a user", False)

        elif data.split()[0] == ':sudo':
            if data.split()[1] == pwd:
                if data.split()[2] == 'cls':
                    global messages
                    messages = []
                    add_message(ip, users[ip] + " cleared history", False)
            else:
                add_message(ip, users[ip] + " tried to type in the admin password.", False)
        elif len(data) == 1 and ord(data) < 30:
            if ord(data) == 1:
                add_message(ip)
            elif ord(data) == 2:
                send = False
                o = count_online()
                self.request.sendall(bytes(str(o), "utf-8"))
            elif ord(data) == 3:
                add_message(ip, "anon [%s] has connected" % ip, False)
                users[ip] = 'anon [%s]' % ip
        else:
            add_message(ip, data)
            print(get_server_time() + ": message from " + ip)
        for message in messages:
            message.update()
            if message.is_message:
                out += str(message) + '\n'
        if send: self.request.sendall(bytes(out, "utf-8"))


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
