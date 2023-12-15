from datetime import datetime
import nmap3
from utils import save_results

def port_scan():
    domain = input('Digite o domínio para a varredura de portas: ')
    nmap = nmap3.Nmap()
    print(f'Iniciando a varredura de portas no domínio {domain}')

    port_range = "21-25,80,443,3306,5432,6379,8080,8443,9200,11211,27017"
    results = nmap.nmap_version_detection(domain, args=f'-p {port_range}')

    port_results = []

    for host, host_info in results.items():
        if isinstance(host_info, dict) and 'ports' in host_info:
            for port_info in host_info['ports']:
                if isinstance(port_info, dict):
                    port = port_info.get('portid')
                    protocol = port_info.get('protocol')
                    state = port_info.get('state', {}).get('state') if isinstance(port_info.get('state'), dict) else port_info.get('state', 'Desconhecido')
                    service = port_info.get('service', {}).get('name', 'Desconhecido')
                    port_result = f'Host: {host} - Porta: {port}/{protocol} - Estado: {state} - Serviço: {service}'
                    print(port_result)
                    port_results.append(port_result)
            else:
                print(f'Não existe porta aberta para {host}')
            if 'state' in host_info and isinstance(host_info['state'], dict):
                host_state = host_info['state'].get('state', 'Desconhecido')
                print(f'Estado do host {host}: {host_state}')
    else:
        print(f'Não existe informações de portas para {host}')

    save = input('Deseja salvar a consulta? (s/n): ')
    if save.lower() == 's':
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        date_to_save = {'port_result': port_results}
        save_results(date_to_save, 'port_result', f'port_scan_{timestamp}.json')         
