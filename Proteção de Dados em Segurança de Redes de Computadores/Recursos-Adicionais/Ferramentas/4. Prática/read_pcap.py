import os
from scapy.all import rdpcap


def read_pcap_path(filepath):
    try:
        packet = rdpcap(filepath)
        for p in packet:
            print(p.summary())

    except FileNotFoundError:
        print(f'Arquivo {filepath} não encontrado')
    
    except Exception as e:
        print(f'Erro ao ler o arquivo - {e}')


def read_pcap_file():
    try:
        files = [f for f in os.listdir('sniffer_result') if f.endswith('.pcap')]
        if not files:
            print('Nenhum arquivo encontrado')
            return
        print('Arquivos disponíveis para consulta: ')
        for i, file in enumerate(files):
            print(f'{i + 1} - {file}')
        
        file_choice = int(input('Escolha o arquivo para consulta: ')) - 1

        if 0 <= file_choice < len(files):
            read_pcap_path(os.path.join('sniffer_result', files[file_choice])),
        else:
            print('Digite uma opção válida')

    except FileNotFoundError:
        print('Não existe diretório sniffer_result')
    except ValueError:
        print('Opção inválida')
    except Exception as e:
        print(f'Erro ao ler o arquivo - {e}')
