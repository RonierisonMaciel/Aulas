from subprocess import Popen, PIPE
import time
from utils import save_result

def organized_output(filename):
    return filename.replace('http://', '').replace('https://', '').replace('/', '').replace('.', '_')

def run_command(command):
    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode(), stderr.decode()

def analyze_sql_injection():
    starttime = time.time()
    url = input("Digite a URL para análise de SQL Injection: ")
    print(f"Executando análise {url} de SQL Injection com Nmap...")
    output, error = run_command(f'sqlmap -u "{url}" --batch --dbs')
    endtime = time.time()
    
    print(f"Tempo de execução: {(endtime - starttime):.2f} segundos.")

    # conclusão, não faço a menor ideia de como voltou a funcionar!

    if error:
        print("Error:", error)
    else:
        print(output)
        save = input("Deseja salvar os resultados? (s/n): ")
        if save.lower() == 's':
            organized = organized_output(url)
            data_to_save = {
                "url": url,
                "output": output
            }
            save_result(data_to_save, "sql_injection_results", f"sql_injection_{organized}.json")
            print(f"Resultados da análise de SQL Injection salvos.")
