# main_script.py
import pyfiglet
import os
from analyze_sql_injection import analyze_sql_injection
from dns_utils import capture_dns_queries
from port_scan_utils import port_scan
from port_test_utils import test_open_ports_from_file

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
                files = os.listdir("port_scan")
                print("\nArquivos disponíveis:")
                for i, file in enumerate(files):
                    print(f"{i + 1} - {file}")
                file_index = int(input("Escolha o número do arquivo: ")) - 1
                if 0 <= file_index < len(files):
                    test_open_ports_from_file(files[file_index])
                else:
                    print("Número de arquivo inválido.")
            except FileNotFoundError:
                print("Pasta 'varredura_portas' não encontrada.")
            except ValueError:
                print("Entrada inválida, por favor digite um número.")
        elif choice == '4':
            analyze_sql_injection()
        elif choice == '5':
            print('XSS')
        elif choice == '6':
            print('Brute Force')
        elif choice == '7':
            print('Packet sniffer')
        elif choice == '8':
            print('Read packets PCAP')
        elif choice == '9':
            break

if __name__ == "__main__":
    main_menu()
