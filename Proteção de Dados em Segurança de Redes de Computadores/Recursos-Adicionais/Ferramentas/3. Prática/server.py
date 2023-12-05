import socket
from cryptography.fernet import InvalidToken
from cryptography.fernet import Fernet

key = b'onCQye5QomMdMtbzqoZreVyWVxbb2mc7ePd0Y6bC6ak='
cipher_source = Fernet(key)

s_host = '0.0.0.0'
s_port = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((s_host, s_port))
server.listen(1)

print(f'O server está ouvindo aqui {s_host} na porta {s_port}')

c_socket, c_address = server.accept()
print(f'Me conectei a {c_address}\n')

message = c_socket.recv(1024)

try:
    decript = cipher_source.decrypt(message).decode()
    print(f'Eu recebi a mensagem -> {decript}')
except InvalidToken:
    print('Falha na autenticação - verifique sua chave.')
    c_socket.close()
except Exception as e:
    print(f'Falha inesperada {e}')
finally:
    server.close()
