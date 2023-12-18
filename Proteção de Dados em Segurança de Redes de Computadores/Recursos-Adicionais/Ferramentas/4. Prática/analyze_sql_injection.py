from subprocess import Popen, PIPE

from utils import save_results


def organize_output(filename):
    return filename.replace('http://', '').replace('https://', '').replace('/', '').replace('.', '_')

def run_command(command):
    process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8'), stderr.decode('utf-8')

def analyze_sql_injection():
    url = input('Digite a url a ser verificada: ')
    print('Verificando se o domínio é vulnerável a SQL Injection...')
    output, error = run_command(f'sqlmap -u "{url}" --batch --dbs')
    
    if error:
        print('Erro ao executar o sqlmap')
    else:
        print(output)
        save = input('Deseja salvar o resultado em um arquivo? (s/n)')
        if save.lower() == 's':
            organize = organize_output(url)
            date_to_save = {
                'url': url,
                'output': output,
                'error': error
            }
            save_results(date_to_save, 'sql_injection', f'sql_inject_{organize}')
            print('Resultado salvo com sucesso!')
