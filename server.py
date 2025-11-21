import socket
import json
import time
import threading
import csv
import os
import random
from queue import Queue


keyword = "gR33tinG$"
selected = False
source_addr = ''
while not selected:
    server_type = input('Running internal or external server?: ')
    match server_type:
        case 'internal':
            temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            temp.connect(("8.8.8.8", 80))
            source_addr = temp.getsockname()[0]
            temp.close()
            selected = True
        case 'external':
            source_addr = socket.gethostbyname(socket.gethostname())
            selected = True
        case _:
            print('invalid entry, options are \'external\' or \'internal\'')

portnum = 3231
fc_seed = int(time.time())
random.seed(fc_seed)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((source_addr, portnum))
print(f'server listening on address {source_addr} on port {portnum}')

client_list = dict()
client_file = 'client_list.csv'

send_queue = Queue()


def initialize():
    if not os.path.exists(client_file):
        with open(client_file, 'w') as cl:
            pass


def get_clients():
    with open(client_file, 'r') as cl:
        cl_csv = csv.reader(cl)
        for row in cl_csv:
            client_list[row[0]] = row[1]


def add_client(addr):
    code = 0
    with open(client_file, 'a') as cl:
        cl_csv = csv.writer(cl)
        code = random.randint(1000000, 1000000000)
        cl_csv.writerow([code, addr])
    get_clients()
    return code


def message_recv():
    server_socket.listen(len(client_list.keys())+1)
    conn, addr = server_socket.accept()
    if addr not in client_list.keys():
        fc = add_client(addr)
        message_send(f'{keyword} {fc}', addr)
        return
    print(f"Connected by {addr}")
    d = conn.recv(1024)
    time.sleep(20)
    msg = json.loads(d.decode('utf-8'))
    friend_code = msg['sendee']
    address = client_list[friend_code]
    msg['sendee'] = address
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
listen_thread.start()
print('system running!')
while True:
    while not send_queue.empty():
        msg = send_queue.get()
        addr = msg['sendee']
        msg_to_send = json.dumps(msg)
        message_send(msg_to_send, addr)
    time.sleep(0.1)