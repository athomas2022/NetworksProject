import socket
import json
import time
import threading
import csv
import os
import random
from queue import Queue


temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
temp.connect(("8.8.8.8", 80))
source_addr = temp.getsockname()[0]
temp.close()

fc_seed = int(time.time())
random.seed(fc_seed)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((source_addr, 3231))

client_list = dict()
client_file = 'client_list.csv'

send_queue = Queue()
lock = threading.Lock()


def initialize():
    if not os.path.exists(client_file):
        with open(client_file, 'w') as cl:
            pass


def get_clients():
    with open(client_file, 'r') as cl:
        with csv.reader(cl) as cl_csv:
            for row in cl_csv:
                client_list[row[0]] = row[1]


def add_client(addr):
    code = 0
    with open(client_file, 'a') as cl:
        with csv.writer(cl) as cl_csv:
            code = random.randint(1000000, 1000000000)
            cl_csv.writerow([code, addr])
    get_clients()
    return code


def message_recv():
    server_socket.listen(len(client_list.keys()))
    conn, addr = server_socket.accept()
    if addr not in client_list.keys():
        fc = add_client(addr)
        message_send(fc, addr)
    print(f"Connected by {addr}")
    d = conn.recv(1024)
    time.sleep(20)
    msg = json.loads(d.decode('utf-8'))
    friend_code = msg['sendee']
    address = client_list[friend_code]
    msg['sendee'] = address
    with lock:
        send_queue.put(msg)


def message_send(message_data, addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('connecting...')
    sock.connect((addr, 12345))
    payload = {"message": message_data, "sendee": source_addr}
    payload_data = json.dumps(payload).encode('utf-8')
    sock.sendall(payload_data)
    sock.close()


print('initializing system...')
initialize()
listen_thread = threading.Thread(target=message_recv, daemon=True)

print('system running!')
while True:
    with lock:
        while not send_queue.empty():
            msg = send_queue.get()
            addr = msg['sendee']
            msg_to_send = json.dumps(msg)
            message_send(msg_to_send, addr)
    time.sleep(0.1)