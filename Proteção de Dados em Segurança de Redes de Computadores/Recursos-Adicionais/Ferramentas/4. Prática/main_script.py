# main_script.py

import os
import pyfiglet
import netifaces
from analyze_sql_injection import analyze_sql_injection
from brute_force import run_hydra
from dns_util import capture_dns_query
from port_scan_utils import port_scan
from port_test_utils import test_open_port_from_file
from read_pcap import read_pcap_file
from sniffer import use_sniffer
from xss_analysis import test_xss


def list_interfaces():
    interfaces = []
    for interface in netifaces.interfaces():
        addr = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addr:
            interfaces.append(interface)
    return interfaces


def main_menu():
    while True:
        header =  pyfiglet.figlet_format('H4CK3R Tools')
        print(header)

        print('1. DNS')
        print('2. Ports')
        print('3. Open Ports')
        print('4. SQL Injection')
        print('5. XSS')
        print('6. Brute Force')
        print('7. Packet Sniffing')
        print('8. Read PCAP')
        print('9. System exit')

        choice = input('Escolha a opção (1-9): ')

        if choice == '1':
            capture_dns_query()
        elif choice == '2':
            port_scan()
        elif choice == '3':
            try:
                files = os.listdir('port_result')
                print('Arquivos disponíveis para consulta: ')
                for i, file in enumerate(files):
                    print(f'{i + 1} - {file}')
                file_index  = int(input('Escolha o arquivo para consulta: ')) - 1
                if 0 <= file_index < len(files):
                    test_open_port_from_file(files[file_index])
                else:
                    print('Opção inválida')
            except FileNotFoundError:
                print('Não existe diretório port_result')
            except ValueError:
                print('Opção inválida')
        elif choice == '4':
            analyze_sql_injection()
        elif choice == '5':
            test_xss()
        elif choice == '6':
            target_url = input('Digite a URL do alvo: ')
            username = input('Digite o usuário: ')
            password = input('Digite a senha: ')
            service_module = input('Digite o módulo do serviço (http-post-form, ssh): ')
            login_page = input('Digite a página de login (ex. login.php): ')
            login_form = input("Digite o formulário de login ('user=^USER^&pass=^PASS^&login=Login') ")
            fail_condition = input('Digite a condição de falha (ex. "incorrect" ou "failed"): ')
            run_hydra(target_url, username, password, service_module, login_page, login_form, fail_condition)
        elif choice == '7':
            interfaces = list_interfaces()
            print('Interfaces disponíveis são: ')
            for i, iface in enumerate(interfaces): #20
                print(f'{i + 1} - {iface}')
            
            iface_index = int(input('Escolha a interface para captura: ')) - 1

            if 0 <= iface_index < len(interfaces):
                interface = list(interfaces)[iface_index]
                filter_expression = input('Digite a expressão de filtro (ex. tcp port 80): ')
                packet_count = int(input('Digite a quantidade de pacotes a serem capturados: '))
                use_sniffer(interface, filter_expression, packet_count)
            else:
                print('Opção inválida - Escolha outra interface')
        elif choice == '8':
            read_pcap_file()
        elif choice == '9':
            print('Saindo do sistema')
            break

if __name__ == "__main__":
    main_menu()
