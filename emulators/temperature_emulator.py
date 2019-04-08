import socket
from random import randint
from time import sleep
import sys

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 9090))
s.listen(1)

while True:
    clientsocket, addr = s.accept()
    print(f"Connection from {addr} has been established.")
    while True:
        random_number = randint(1,15)
        msg = f"{random_number}"
        msg = f"{len(msg):<{HEADERSIZE}}"+msg
        print(msg)
        clientsocket.send(bytes(msg,"utf-8"))

