import argparse
import ctypes
import os
import socket
import threading
import time

import unicurses as u

parser = argparse.ArgumentParser(description="Open a client connected to an ip.")
parser.add_argument('host', default='localhost', nargs='?', help='server host address')
parser.add_argument('port', default='80', type=int, nargs='?', help='server host post')
parser.add_argument('-c', '--channel', default='lobby')
parser.add_argument('-u', '--user', default='anon')


args = parser.parse_args()

kill_thread = False
HOST, PORT = args.host, args.port
channel = args.channel

os.system("mode con: cols=120 lines=30")

m_to_display = 22


def draw_boxes():
    u.box(chat_win)
    u.box(input_win)
    u.box(people_win)


def reset():
    u.wclear(chat_win)
    u.wclear(input_win)
    u.wclear(people_win)


def refresh():
    draw_boxes()
    u.wrefresh(chat_win)
    u.wrefresh(input_win)
    u.wrefresh(people_win)


def get_latest(l):
    if len(l) < m_to_display:
        return l
    else:
        return l[-m_to_display:]


def get_messages():
    old_messages = ''
    while True:
        if kill_thread:
            break
        time.sleep(0.05)
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((HOST, PORT))
                sock.sendall(bytes(channel + chr(0) + chr(2), "utf-8"))
                recvd = sock.recv(1024).decode().split('||')
                count = recvd[0]
                users = recvd[1].split('|')
                ctypes.windll.kernel32.SetConsoleTitleA(bytes(channel + ": " + str(count) + " user(s) online", "utf-8"))
                u.wclear(people_win)
                u.box(people_win)
                i = 1
                u.mvwaddstr(people_win, i, 1, ' Users in #%s:' % channel)
                for user in users:
                    i += 1
                    u.mvwaddstr(people_win, i, 1, '  - ' + user)
                u.wrefresh(people_win)
                sock = socket.socket()
                sock.connect((HOST, PORT))
                break
            except (ConnectionRefusedError, ConnectionResetError):
                u.mvwaddstr(chat_win, 1, 1, "Can't connect.")
                time.sleep(1)
        sock.sendall(bytes(channel + chr(0) + chr(1), "utf-8"))
        incoming_messages = str(sock.recv(4096), "utf-8")
        if not incoming_messages == old_messages:
            i = 0
            u.wclear(chat_win)
            draw_boxes()
            for message in get_latest(incoming_messages.split('\n')):
                i += 1
                u.mvwaddstr(chat_win, i, 1, message[:78])
            u.wrefresh(chat_win)
            old_messages = incoming_messages
        time.sleep(0.1)


message_refresh_thread = threading.Thread(target=get_messages)

err = []
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        sock.connect((HOST, PORT))
    except WindowsError:
        print("Can't connect: " + HOST + ':' + str(PORT))
        continue
    break
sock.sendall(bytes(channel + chr(0) + chr(3) + chr(0) + args.user, "utf-8"))
stdscr = u.initscr()
u.curs_set(0)
chat_win = u.newwin(25, 90, 0, 0)
input_win = u.newwin(5, 90, 25, 0)
people_win = u.newwin(30, 30, 0, 90)
message_refresh_thread.start()
while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    u.wclear(input_win)
    u.mvwaddstr(input_win, 1, 1, '> ')
    refresh()
    u.flushinp()
    data = u.mvwgetstr(input_win, 1, 3)
    send = True

    if data in [":exit", "^C", ":quit", ":q"]:
        break
    if send:
        try:
            sock.connect((HOST, PORT))
            sock.sendall(bytes(channel + chr(0) + data + "\n", "utf-8"))
        except (ConnectionRefusedError, ConnectionResetError):
            err.append("Can't connect.")
        finally:
            sock.close()
    if len(data.split()) > 1:
        if data.split()[0] == ":join":
            try:
                channel = data.split()[1]
            except IndexError:
                pass
    refresh()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
sock.sendall(bytes(channel + chr(0) + chr(4) + "\n", "utf-8"))
u.endwin()
# noinspection PyRedeclaration
kill_thread = True
time.sleep(0.1)
os.system('cls')
