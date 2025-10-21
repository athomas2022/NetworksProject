import socket
import threading
import json


# source_name = socket.gethostname()
# source_addr = socket.gethostbyname(source_name)
temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
temp.connect(("8.8.8.8", 80))
source_addr = temp.getsockname()[0]
temp.close()
print(source_addr)
test_dest = '163.118.57.142'


def message_send(message_data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('connecting...')
    sock.connect((test_dest, 12345))
    payload = {"message": message_data, "value": 123}
    payload_data = json.dumps(payload).encode('utf-8')
    sock.sendall(payload_data)
    sock.close()


def message_recv():
    print('running')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('163.118.57.142', 12345))
    print('listening...')
    s.listen(1)
    print('accepting...')
    conn, addr = s.accept()
    print(f"Connected by {addr}")
    d = conn.recv(1024)
    print(d.decode('utf-8'))


msg_data = "Hello World!"

#sniff_thread = threading.Thread(target=message_receive)
#send_thread = threading.Thread(target=message_send, args=(msg_data,))

#sniff_thread.start()
#send_thread.start()

message_send(msg_data)
