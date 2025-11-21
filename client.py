import socket
import json
import time


# source_name = socket.gethostname()
# source_addr = socket.gethostbyname(source_name)
temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
temp.connect(("8.8.8.8", 80))
source_addr = temp.getsockname()[0]
temp.close()
test_dest = '163.118.57.142'
contact_count = 1
server_mode = False

recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
recv_socket.bind((source_addr, 12345))


def update_server_mode(mode):
    global server_mode
    server_mode = mode


def get_server_mode():
    global server_mode
    return server_mode


def update_cc(updated_cc):
    global contact_count
    contact_count = updated_cc

def message_send(message_data, dest):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('connecting...')
    sock.connect((dest, 3231))
    payload = {"message": message_data, "sendee": dest}
    payload_data = json.dumps(payload).encode('utf-8')
    sock.sendall(payload_data)
    sock.close()


def message_recv():
    print('running')
    print('listening...')
    recv_socket.listen(contact_count)
    print('accepting...')
    conn, addr = recv_socket.accept()
    print(f"Connected by {addr}")
    d = conn.recv(1024)
    time.sleep(20)
    return d.decode('utf-8')

