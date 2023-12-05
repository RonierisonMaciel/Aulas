
import socket
from cryptography.fernet import Fernet

key = b'onCQye5QomMdMtbzqoZreVyWVxbb2mc7ePd0Y6bC6ak='
cipher_source = Fernet(key)

c_host = '10.88.0.3'
c_port = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((c_host, c_port))

message = 'Olá server!' # 1. passei para o parâmetro message
cripto = cipher_source.encrypt(message.encode()) # 2. encriptei a mensagem
client.send(cripto) # 3. enviei a mensagem criptografada
client.close()
