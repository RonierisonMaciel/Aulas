from scapy.all import sniff, DNSQR, DNSRR
from datetime import datetime
import time

def safe_decode(data):
    if isinstance(data, bytes):
        try:
            return data.decode('utf-8')
        except UnicodeDecodeError:
            return repr(data)
    else:
        return data


def capture_dns_queries():
    dns_queries = []
    start_time = time.time()

    def packet_callback(packet):
        if packet.haslayer(DNSQR):
            dns_query_layer = packet[DNSQR]
            query_info = {
                'query_name': safe_decode(dns_query_layer.qname) if dns_query_layer.qname else 'Desconhecido',
                'query_type': dns_query_layer.qtype,
                'response': []
            }

            if packet.haslayer(DNSRR):
                for i in range(packet[DNS].ancount):
                    rr = packet[DNSRR][i]
                    response_name = safe_decode(rr.rrname) if rr.rrname else 'Desconhecido',
                    response_data = safe_decode(rr.rdata) if rr.rdata else 'Desconhecido'
                    query_info['response'].append({
                        'response_name': response_name,
                        'response_type': rr.type,
                        'response_data': response_data,
                        'response_ttl': rr.ttl
                    })
            dns_queries.append(query_info)
    #-----
    print('Capturando consultas DNS')
    sniff(filter='port 53', prn=packet_callback, store=0)
    #-----

    end_time = time.time()
    capture_duration = end_time - start_time

    print(f'Captura finalizada - com duração {capture_duration}, com total de {len(dns_queries)} consultas.')

