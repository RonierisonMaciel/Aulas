import socket

t_host = '127.0.0.1'
t_port = 5001

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((t_host, t_port))
client.send(f'\n Olá, boa tarde {t_host}!'.encode())
client.close()
