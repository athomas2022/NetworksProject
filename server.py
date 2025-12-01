import socket
import json
import time
import threading
import csv
import os
import random
from queue import Queue
import socketserver


class ThreadedAydegerServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True


class AydegerServer(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.keyword = "gR33tinG$"
        self.portnum = 3231
        fc_seed = int(time.time())
        random.seed(fc_seed)
        # self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server_socket.bind((self.source_addr, self.portnum))
        # print(f'server listening on address {self.source_addr} on port {self.portnum}')

        self.client_list = dict()
        self.client_file = 'client_list.csv'

        self.send_queue = Queue()

        if not os.path.exists(self.client_file):
            with open(self.client_file, 'w') as cl:
                pass
        self.get_clients()
        super().__init__(request, client_address, server)

    def get_clients(self):
        with open(self.client_file, 'r') as cl:
            cl_csv = csv.reader(cl)
            for row in cl_csv:
                if len(row) == 2:
                    print(f'{len(row)}: {row}')
                    self.client_list[row[0]] = row[1]

    def add_client(self, addr):
        code = 0
        with open(self.client_file, 'a') as cl:
            cl_csv = csv.writer(cl)
            code = random.randint(1000000, 1000000000)
            cl_csv.writerow([code, addr])
        self.get_clients()
        return code

    def message_recv(self):
        while True:
            print(len(self.client_list.keys()))
            self.server_socket.listen(len(self.client_list.keys())+1)
            conn, addr_raw = self.server_socket.accept()
            addr = addr_raw[0] #addr_raw[addr_raw.index('(')+1:addr_raw.index(',')]
            if addr not in self.client_list.values():
                fc = self.add_client(addr)
                self.message_send(f'{self.keyword} {fc}', addr)
                return
            print(f"Connected by {addr}")
            d = conn.recv(1024)
            msg = json.loads(d.decode('utf-8'))
            if self.keyword in msg['message']:
                for k, v in self.client_list.items():
                    if v == addr:
                        self.message_send(f'{self.keyword} {k}', addr)
                        return
            friend_code = msg['sendee']
            address = self.client_list[friend_code]
            msg['sendee'] = address
            self.send_queue.put(msg)
            conn.close()

    def message_send(self, message_data, addr, snd=''):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('connecting...')
        sock.connect((addr, 12345))
        print(f'connected to {addr}!')
        print(f'sending to {addr} from {snd}')
        payload = {"message": message_data, "sendee": addr, 'sender': snd}
        payload_data = json.dumps(payload).encode('utf-8')
        sock.sendall(payload_data)
        sock.close()

    def handle(self):
        addr = self.client_address[0]
        if addr not in self.client_list.values():
            fc = self.add_client(addr)
            self.message_send(f'{self.keyword} {fc}', addr)
            print('sent fc!')
            return
        while True:
            data = self.request.recv(1024).strip()
            if not data:
                break
            msg = json.loads(data.decode('utf-8'))
            if self.keyword in msg['message']:
                for k, v in self.client_list.items():
                    if v == addr:
                        self.message_send(f'{self.keyword} {k}', addr)
                        return
            friend_code = msg['sendee'].strip()
            address = self.client_list[friend_code]
            msg['sendee'] = address
            self.message_send(msg['message'], address, msg['sender'])


print('initializing system...')
#listen_thread = threading.Thread(target=message_recv, daemon=True)
#listen_thread.start()
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

with ThreadedAydegerServer((source_addr, 3231), AydegerServer) as server:
    print('system running!')
    server.serve_forever()
# while True:
#     while not send_queue.empty():
#         msg = send_queue.get()
#         addr = msg['sendee']
#         msg_to_send = json.dumps(msg)
#         message_send(msg_to_send, addr)
#     time.sleep(0.05)
