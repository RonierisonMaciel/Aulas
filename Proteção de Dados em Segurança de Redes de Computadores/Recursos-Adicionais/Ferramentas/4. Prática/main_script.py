# main_script.py

import os
from analyze_sql_injection import analyze_sql_injection
from dns_util import capture_dns_query
from port_scan_utils import port_scan
from port_test_utils import test_open_port_from_file

def main_menu():
    while True:
        print('1. DNS')
        print('2. Ports')
        print('3. Open Ports')
        print('4. SQL Injection')
        print('5. XSS')
        print('6. Brute Force')
        print('7. Packet Sniffing')
        print('8. Read PCAP')
        print('9. System exit')

        choice = input('Escolha a opção (1-9)')

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
            print('XSS')
        elif choice == '6':
            print('Brute Force')
        elif choice == '7':
            print('Packet Sniffing')
        elif choice == '8':
            print('Read PCAP')
        elif choice == '9':
            print('Saindo do sistema')
            break

if __name__ == "__main__":
    main_menu()
