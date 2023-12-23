# main_script.py
import pyfiglet
import os
import netifaces
from analyze_sql_injection import analyze_sql_injection
from brute_force import run_hydra
from dns_utils import capture_dns_queries
from port_scan_utils import port_scan
from port_test_utils import test_open_ports_from_file
from read_pcap import read_pcap_files
from use_packet import use_capture
from xss_analysis import test_xss

def list_network_interfaces():
    interfaces = []
    for interface in netifaces.interfaces():
        addr = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addr:
            interfaces.append(interface)
    return interfaces

def select_file_from_folder(folder):
    try:
        files = os.listdir(folder)
    except FileNotFoundError:
        print(f"Pasta '{folder}' não encontrada.")
        return None

    print(f"\nArquivos disponíveis em {folder}:")
    for i, file in enumerate(files):
        print(f"{i + 1} - {file}")
    file_index = int(input(f"Escolha o número do arquivo de {folder}: ")) - 1

    if 0 <= file_index < len(files):
        return os.path.join(folder, files[file_index])
    else:
        print("Número de arquivo inválido.")
        return None

def main_menu():
    while True:

        header = pyfiglet.figlet_format("Pentest Tools")
        
        print(header)

        print('-----------------------------------')
        print('1. DNS')
        print('2. Ports')
        print('3. Open ports')
        print('4. SQL Injection')
        print('5. XSS')
        print('6. Brute Force')
        print('7. Packet sniffer')
        print('8. Read packets PCAP')
        print('9. Exit')
        print('----------------------------------')

        choice = input('Escolha um número (1-9): ')

        if choice == '1':
            capture_dns_queries()
        elif choice == '2':
            port_scan()
        elif choice == '3':
            try:
                files_pass = os.listdir("port_scan")
                print("\nArquivos disponíveis:")
                for i, file in enumerate(files_pass):
                    print(f"{i + 1} - {file}")
                file_index = int(input("Escolha o número do arquivo: ")) - 1
                if 0 <= file_index < len(files_pass):
                    test_open_ports_from_file(files_pass[file_index])
                else:
                    print("Número de arquivo inválido.")
            except FileNotFoundError:
                print("Pasta 'varredura_portas' não encontrada.")
            except ValueError:
                print("Entrada inválida, por favor digite um número.")
        elif choice == '4':
            analyze_sql_injection()
        elif choice == '5':
            test_xss()
        elif choice == '6':
            password_file_path = select_file_from_folder("passwords")
            user_file_path = select_file_from_folder("users")
            if password_file_path and user_file_path:
                target_url = input('Digite a URL ou IP do alvo: ')
                service_module = input('Digite o módulo do serviço (ex: http-form-post): ')
                login_page = input('Digite a página de login (ex: /userinfo.php): ')
                params1 = input('Digite o primeiro parâmetro (ex: username): ')
                params2 = input('Digite o segundo parâmetro (ex: password): ')
                fail_condition = input('Digite a condição de falha (login page): ')
                print('\n')
                run_hydra(target_url, user_file_path, password_file_path, service_module, login_page, params1, params2, fail_condition)
            else:
                print("Erro ao selecionar os arquivos de usuário e senha.")
        elif choice == '7':
            interfaces = list_network_interfaces()
            print('Interfaces disponíveis:')
            for i, inface in enumerate(interfaces):
                print(f'{i + 1} - {inface}')

            iface_choice = int(input('Escolha uma interface: ')) - 1
            if 0 <= iface_choice < len(interfaces):
                interface = list(interfaces)[iface_choice]
                filter_expression = input('Digite a expressão de filtro (ex: port 80): ')
                packet_count = int(input('Digite a quantidade de pacotes a serem capturados: '))
                use_capture(interface, filter_expression, packet_count)
            else:
                print('Escolha uma interface válida.')
        elif choice == '8':
            read_pcap_files()
        elif choice == '9':
            break

if __name__ == "__main__":
    main_menu()
