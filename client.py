from scapy.layers.inet import IP, Ether, TCP
from scapy.packet import Raw
from scapy.config import conf
from scapy.sendrecv import sendp, send, sniff
import socket


source_name = socket.gethostname()
source_addr = socket.gethostbyname(source_name)
test_dest = source_addr


def message_send(message_data):
    ip_layer = make_ip_layer(source_addr, test_dest)
    payload = Raw(load=message_data)
    complete_packet = ip_layer / payload
    send(complete_packet)


def make_ip_layer(srca, dsta):
    return IP(src=srca, dst=dsta)


def message_receive():
    def recv_protocol(packet):
        if test_dest in packet:
            if Raw in packet:
                return packet[Raw].load
            else:
                return 'packet found but no payload'

    print(sniff(prn=recv_protocol, store=0))


msg_data = "Hello World!"
message_send(msg_data)
