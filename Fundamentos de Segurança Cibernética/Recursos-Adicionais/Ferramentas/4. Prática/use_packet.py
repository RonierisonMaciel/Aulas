from datetime import datetime
from scapy.all import sniff, wrpcap

from utils import save_result

def use_capture(interface, filter_expression, packet_count):
    capture_packets = []

    def packet_handler(packet):
        print(packet.show())
        capture_packets.append(packet)

    try:
        print(f'Estou iniciando a captura de pacotes na interface {interface}. Pressione Ctrl+C para finalizar')
        sniff(iface=interface, filter=filter_expression, prn=packet_handler, count=packet_count)
    except Exception as e:
        print(f"Houve o seguinte erro ao capturar pacotes: {e}")
    finally:
        save = input('Deseja salvar os pacotes capturados? (s/n): ')
        if save.lower() == 's':
            timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            file_name = f'captura_{interface}_{timestamp}.pcap'
            wrpcap(file_name, capture_packets)
            save_result(file_name, 'packet_output', f'capturas_{interface}_{timestamp}.pcap')
            print(f'Captura finalizada. Foram capturados {len(capture_packets)} pacotes. \
                  Para visualizar os pacotes capturados, use a opção 8 do menu principal.')
