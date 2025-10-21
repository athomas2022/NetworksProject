from scapy.layers.inet import IP, Ether, TCP, UDP
from scapy.packet import Raw
from scapy.config import conf
from scapy.sendrecv import sendp, send, sniff
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
    eth = Ether(dst="ff:ff:ff:ff:ff:ff")
    ip_layer = make_ip_layer(source_addr, test_dest)
    payload = Raw(load=message_data)
    complete_packet = eth / ip_layer / TCP(sport=1234, dport=4445, flags="PA") / payload
    complete_packet.show()
    sendp(complete_packet)


def send_2(message_data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('connecting...')
    sock.connect((test_dest, 12345))
    payload = {"message": message_data, "value": 123}
    payload_data = json.dumps(payload).encode('utf-8')
    sock.sendall(payload_data)
    sock.close()




def make_ip_layer(srca, dsta):
    return IP(src=srca, dst=dsta)


def message_receive():
    def recv_protocol(packet):
        if Raw in packet:
             print(packet[Raw].load)
        else:
            print('packet found but no payload')

    print(sniff(prn=recv_protocol, filter=f'src {source_addr} and dst {test_dest}', count=1))


def sock_recv():
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

send_2(msg_data)
