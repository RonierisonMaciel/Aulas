import json
import os
import shutil

def save_result(data, folder, filename):
    
    if not os.path.exists(folder):
        os.makedirs(folder)

    filepath = os.path.join(folder, filename)

    if isinstance(data, str) and os.path.isfile(data):
        shutil.move(data, filepath)
    else:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    
    print(f'Salvo com sucesso na pasta {filepath}')
