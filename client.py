import scapy
from scapy.layers.inet import IP, Ether, TCP
from scapy.packet import Raw
from scapy.config import conf
from scapy.sendrecv import sendp, send, sniff
import socket
from time import sleep


source_name = socket.gethostname()
source_addr = socket.gethostbyname(source_name)
test_dest = '163.118.57.184'


def message_send(message_data):
    ip_layer = make_ip_layer(source_addr, test_dest)
    payload = Raw(load=message_data)
    complete_packet = ip_layer / payload
    send(complete_packet)


def make_ip_layer(srca, dsta):
    return IP(src=srca, dst=dsta)


def message_receive():
    def recv_protocol(packet):
        if Raw in packet:
            packet.summary()
            print(packet[Raw].load)#.decode('utf-8', errors='replace'))
        else:
            print('packet found but no payload')

    capture = sniff(prn=recv_protocol, filter='src 163.118.57.184 and dst 163.118.57.142', count=1)
    capture.summary()


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
