from datetime import datetime
from scapy.all import sniff, wrpcap

from utils import save_results


def use_sniffer(interface, filter_expression, packet_count):
    captured_packets = []

    def packet_handler(packet):
        print(packet.show())
        captured_packets.append(packet)

    try:
        print(f'Iniciando a captura de pacotes na rede na interface {interface}. Pressione CTRL+C para interromper.')
        sniff(iface=interface, filter=filter_expression, prn=packet_handler, count=packet_count)
    except Exception as e:
        print(f'Erro ao capturar pacotes: {e}')
    except KeyboardInterrupt:
        print('Interrompendo a captura de pacotes')
    finally:
        save = input('Deseja salvar os pacotes capturados? (s/n): ')
        if save.lower() == 's':
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
            file_name = f'captured_pck{timestamp}.pcap'
            wrpcap(file_name, captured_packets)
            save_results(file_name, 'sniffer_result', f'packet_sniff_{interface}_{timestamp}.pcap')
            print(f'Arquivo {file_name} salvo com sucesso \
                  use a opção 8 para ler o arquivo.')
