import os
from scapy.all import rdpcap

def read_pcap_file(filepath):
    try:
        packets = rdpcap(filepath)

        for packet in packets:
            print(packet.summary())
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")

def read_pcap_files():
    try:
        files = [f for f in os.listdir("packet_output") if f.endswith(".pcap")]
        
        if not files:
            print("Não há arquivos de captura.")
            return
        
        print('Os arquivos disponíveis são: ')
        for i, file in enumerate(files):
            print(f"{i + 1} - {file}")

        file_choice = int(input("Escolha o número do arquivo: ")) - 1

        if 0 <= file_choice < len(files):
            read_pcap_file(os.path.join("packet_output", files[file_choice]))
        else:
            print("Número de arquivo inválido.")
    except FileNotFoundError:
        print("Pasta 'packet_output' não encontrada.")
    except Exception as e:
        print(f"Erro ao ler arquivos: {e}")

