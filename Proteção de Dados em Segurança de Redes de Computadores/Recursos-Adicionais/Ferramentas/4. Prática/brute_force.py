import subprocess

from utils import save_results

def run_hydra(target_url, username, password, service_module, login_page, login_form, fail_condition):
    try:
        print(f'O serviço em operação com Hydra é: {service_module}')

        command = f"hydra -l {username} -p {password} {service_module}:// {target_url} '{login_page}:{login_form}:{fail_condition}'"
        # resolver essa questão da requisição do USER e PASS

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if 'Status password incorrect' in stdout.decode():
            print('Login inválido')
        else:
            print('Login válido')
            print(stdout.decode())

            save = input('Deseja salvar o resultado? (s/n): ')
            if save.lower() == 's':
                save_results(stdout.decode(), 'hydra_results', f'hydra_{service_module}_{target_url}.txt')
                print('Resultado salvo com sucesso!')
    
    except Exception as e:
        print(f'Problema com o Hydra: {e}')
