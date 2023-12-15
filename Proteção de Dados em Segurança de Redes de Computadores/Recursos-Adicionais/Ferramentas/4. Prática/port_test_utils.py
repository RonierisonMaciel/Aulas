from datetime import datetime
import json
import socket
from utils import save_results

def send_service_probe(socket, port):
    commands = {
        80: b"HEAD / HTTP/1.0\r\n\r\n",
        22: b"SSH-2.0-test\r\n",
        443: b"HEAD / HTTP/1.0\r\n\r\n",
        1433: b"SELECT @@VERSION\r\n",
        3306: b"SELECT @@VERSION\r\n",
        5432: b"SELECT version();\r\n",
        6379: b"PING\r\n",
        8080: b"HEAD / HTTP/1.0\r\n\r\n",
        8443: b"HEAD / HTTP/1.0\r\n\r\n",
        9200: b"GET /\r\n",
        11211: b"version\r\n",
        27017: b"ismaster\r\n",
        # Adicionar mais comandos aqui
    }

    command = commands.get(port, None)
    if command:
        socket.sendall(command)
        socket.send

def test_open_port(ip_address, port, timeout=5):
    service_response = "Sem resposta do serviço"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip_address, port))
            if result == 0:
                try:
                    send_service_probe(s, port)
                    service_response = s.recv(1024).decode('utf-8', 'ignore')
                except socket.error:
                    service_response = "Erro ao interagir com o serviço"
                return f"Porta {port}: Aberta - Resposta: {service_response}"
            else:
                return f"Porta {port}: Fechada ou filtrada"
    except socket.error as e:
        return f"Porta {port}: Erro ao testar - {e}"

def test_open_port_from_file(filename):
    file_path = f'port_result/{filename}'
    test_results = []
    try:
        with open(file_path, 'r') as file:
            port_data = json.load(file)

        for entry in port_data['port_result']:
            parts = entry.split(' - ')
            host = parts[0].split(': ')[1]
            port = int(parts[1].split('/')[0].split(': ')[1])
            state = parts[2].split(': ')[1]

            if state == 'open':
                test_result = test_open_port(host, port)
                print(test_result)
                test_results.append(test_result)
            
        save = input('Deseja salvar a consulta? (s/n): ')
        if save.lower() == 's':
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            date_to_save = {f'response_port': test_result}
            save_results(date_to_save, 'response_ports', f'port_scan_{timestamp}.json')
    
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f'Não foi possível ler o arquivo {file_path} - {e}')
    except Exception as e:
        print(f'Erro inesperado: {e}')
