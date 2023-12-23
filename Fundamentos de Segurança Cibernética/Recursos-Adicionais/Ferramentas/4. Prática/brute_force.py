import os
import re
import subprocess

from utils import save_result

def run_hydra(target_url, user_file_path, pass_file_path, service_module, login_page, params1, params2, fail_condition):
    try:
        hydra_output_file = "hydra_result.txt"
        command = f"hydra {target_url} {service_module} "\
                  f"\"/{login_page}:{params1}=^USER^&={params2}^PASS^:{fail_condition}\" -L {user_file_path} -P {pass_file_path} -V -o {hydra_output_file}"

        # Executa o Hydra e aguarda a finalização
        subprocess.run(command, shell=True, check=True)

        # Verifica se o arquivo de resultados do Hydra foi criado
        if os.path.exists(hydra_output_file):
            # Processa o arquivo de resultados do Hydra
            with open(hydra_output_file, 'r') as file:
                hydra_output = file.read()

            # Procura por combinações bem-sucedidas de usuário e senha
            success_pattern = re.compile(r"login:\s*(.*?)\s*password:\s*(.*?)$")
            matches = success_pattern.findall(hydra_output)
            if matches:
                for username, password in matches:
                    print(f"Combinação bem-sucedida encontrada: {username} / {password}")

                # Opção para salvar os resultados
                save_option = input("Deseja salvar os resultados? (s/n): ")
                if save_option.lower() == 's':
                    save_result(matches, "hydra_results", f"hydra_{target_url.replace('/', '_')}.json")
                    print("Resultados salvos.")
            else:
                print("Nenhuma combinação bem-sucedida encontrada.")
        else:
            print("Arquivo de resultados do Hydra não encontrado.")

    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar Hydra: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
