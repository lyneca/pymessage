import unicurses as u
import os
import time
import socket
import ctypes
import threading

HOST, PORT = "10.26.142.14", 80

os.system("mode con: cols=100 lines=30")

m_to_display = 22

stdscr = u.initscr()
u.curs_set(0)
chat_win = u.newwin(25, 80, 0, 0)
input_win = u.newwin(5, 80, 25, 0)
people_win = u.newwin(30, 20, 0, 80)


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
        time.sleep(0.05)
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
                u.mvwaddstr(chat_win, 1, 1, "Can't connect.")
                time.sleep(1)
        sock.sendall(bytes(chr(1), "utf-8"))
        incoming_messages = str(sock.recv(4096), "utf-8")
        if not incoming_messages == old_messages:
            i = 0
            u.wclear(chat_win)
            draw_boxes()
            for message in get_latest(incoming_messages.split('\n')):
                i += 1
                u.mvwaddstr(chat_win, i, 1, message)
            u.wrefresh(chat_win)
            old_messages = incoming_messages
        time.sleep(0.1)


message_refresh_thread = threading.Thread(target=get_messages)

message_refresh_thread.start()
err = []
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
sock.sendall(bytes(chr(3), "utf-8"))
while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    u.wclear(input_win)
    u.mvwaddstr(input_win, 1, 1, '> ')
    refresh()
    u.flushinp()
    data = u.mvwgetstr(input_win, 1, 3)
    try:
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data + "\n", "utf-8"))
    except (ConnectionRefusedError, ConnectionResetError):
        err.append("Can't connect.")
    finally:
        sock.close()
        refresh()

u.getstr([10, 10])
