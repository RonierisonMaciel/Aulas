from datetime import datetime
import json
import socket

from utils import save_result


def send_service_probe(socket, port):
    commands = {
        80: b'HEAD / HTTP/1.1\r\r\n\r\n',
        22: b'SSH-2.0-OpenSSH_7.2p2 Ubuntu-4ubuntu2.8\r\n',
        21: b'USER anonymous\r\n',
        443: b'HEAD / HTTP/1.1\r\n\r\n',
        3306: b'\x00\x00\x00\x1a\x01\x85\x0a\x00\x00\x00\x00\x00\x00\x00\x01\x08\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00mysql_native_password\x00',
        27017: b'\x00\x00\x00\x00\x00\x00\x00\x00\x74\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00admin.$cmd\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00\x01\x00\x00\x00\x10\x69\x73\x4d\x61\x73\x74\x65\x72\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x66\x69\x6e\x64\x00\x1a\x00\x00\x00\x01\x00\x00\x00\x08\x6c\x69\x73\x74\x44\x61\x74\x61\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        8443: b'HEAD / HTTP/1.1\r\n\r\n',
    }
    
    command = commands.get(port, None)
    if command:
        socket.sendall(command)

def test_open_port(ip_address, port, timeout=5):
    service_response = 'Sem resposta do serviço'
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip_address, port))
            if result == 0:
                try:
                    send_service_probe(s, port)
                    service_response = s.recv(1024).decode('utf-8', 'ignore')
                except socket.error:
                    service_response = 'Não obtive respostas do serviço'
                return f'Porta {port}: Aberta - Resposta: {service_response}'
            else:
                return f'Porta {port}: Fechada ou Filtrada'
    except socket.error as e:
        return f'Porta {port}: Erro ao testar - {e}'
    
def test_open_ports_from_file(filename):
    file_path = f'port_scan/{filename}'
    test_results = []

    try:
        with open(file_path, 'r') as file:
            port_data = json.load(file)

        for entry in port_data['port_results']:
            parts = entry.split(' - ')
            host = parts[0].split(': ')[1]
            port = int(parts[1].split('/')[0].split(': ')[1])
            state = parts[2].split(': ')[1]

            if state == 'open':
                test_result = test_open_port(host, port)
                print(test_result)
                test_results.append(test_result)

        save = input('Deseja salvar o resultado? (s/n)')
        
        if save.lower() == 's':
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            date_to_save = {'port_open_results': test_results}
            save_result(date_to_save, 'ports_verify', f'port_open_results_{timestamp}.json')

    except (FileNotFoundError,  json.JSONDecodeError) as e:
        print(f'Erro ao processar e abrir o arquivo {file_path}: {e}')
    except Exception as e:
        print(f'Erro desconhecido: {e}')
            
