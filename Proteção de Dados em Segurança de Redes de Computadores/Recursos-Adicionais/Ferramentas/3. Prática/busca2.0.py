import nmap3
import dns.resolver
from scapy.all import sniff
import json

nmap = nmap3.Nmap()

def nmap_scan(ip):
    try:
        scan_result = nmap.scan_top_ports(ip, args="-p 20-1025")
        open_ports = [port for port in scan_result[ip]["ports"] if port["state"] == "open"]
        return open_ports
    except Exception as e:
        return str(e)

def dns_query(ip):
    try:
        resutl = dns.resolver.resolve(ip, "PTR")
        return [rdata.to_text() for rdata in resutl]
    except Exception as e:
        return str(e)


""" def capture_package(packet):
    return packet.haslayer("TCP") and packet.haslayer("IP") and \
        (packet["TCP"].dport == 80 or packet["TCP"].dport == 443)
"""
def request_packet(packet):
    if packet.haslayer("IP"):
        ip = packet["IP"].src
        open_ports = nmap_scan(ip)
        dns_info = dns_query(ip)
        packet_info = {
            "src_ip": ip,
            "open_port": open_ports,
            "dns_info": dns_info
        }
        print(packet_info)
        return packet_info
    else:
        return None


def sniff_traffic():
    packets = sniff(filter="ip", count=50)
    http_packets = [request_packet(packet) for packet in packets if capture_package(packet)]

    with open("output.json", "w") as file:
        json.dump([pkt for pkt in http_packets if pkt], file, indet=4)

    
sniff_traffic()

