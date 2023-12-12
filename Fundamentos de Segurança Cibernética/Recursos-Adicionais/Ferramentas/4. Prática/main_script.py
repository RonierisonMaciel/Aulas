# main_script.py

from dns_utils import capture_dns_queries

def main_menu():
    while True:

        print('1. Consultas DNS')
        print('2. Sair')

        choice = input('Escolha um número')

        if choice == '1':
            capture_dns_queries()
        if choice == '2':
            break

if __name__ == "__main__":
    main_menu()
