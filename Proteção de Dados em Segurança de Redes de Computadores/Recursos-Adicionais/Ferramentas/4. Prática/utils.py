import json
import os
import shutil

def save_results(data, folder, file_name):
    if not os.path.exists(folder):
        os.makedirs(folder)

    filepath = os.path.join(folder, file_name)

    if isinstance(data, str) and os.path.isfile(data):
        shutil.copyfile(data, filepath)
    else:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    
    print(f'Os resultados foram salvos em {filepath}')
