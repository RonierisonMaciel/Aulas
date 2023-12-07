from scapy.all import sniff
import json


def capture_package(packet):
    return packet.haslayer("TCP") and packet.haslayer("IP") and \
        (packet["TCP"].dport == 80 or packet["TCP"].dport == 443)

def request_packet(packet): 
    if capture_package(packet):
        packet_info = {
            "src_ip": packet["IP"].src,
            "dst_ip": packet["IP"].dst,
            "src_port": packet["TCP"].sport,
            "dst_port": packet["TCP"].dport
        }
        print(packet_info)
        return packet_info
    else:
        return None


def sniff_traffic():
    packets = sniff(filter="tcp", count=50)
    http_packets = [request_packet(packet) for packet in packets if capture_package(packet)]

    with open("output.json", "w") as file:
        json.dump([pkt for pkt in http_packets if pkt], file, indet=4)

    
sniff_traffic()

