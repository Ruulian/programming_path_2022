import socket
import re

skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "0xhorizon.eu"
port = 16771

skt.connect((host, port))

while 1:
    data = skt.recv(9999999).decode()
    
    if data != '':
        print(data)
        if "=" in data:
           numbers = re.findall(r"-?\d{1,2}", data)
           result = round(int(numbers[1])/int(numbers[0]), 1)
           skt.send(str(result).encode() + b"\n")