import socket

s_host = '0.0.0.0'
s_port = 5001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((s_host, s_port))
server.listen(1)

print(f'Eu estou ouvindo no {s_host} na porta {s_port}')

c_socket, c_address = server.accept()
print(f'A conexão com {c_address} foi realizada')

message = c_socket.recv(1024)
print(f'\n A mensagem enviada foi {message.decode()}')

c_socket.close()
server.close()
