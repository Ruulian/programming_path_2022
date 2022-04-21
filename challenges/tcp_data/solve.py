import socket

skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "0xhorizon.eu"
port = 16772

skt.connect((host, port))

while 1:
    data = skt.recv(9999999).decode()
    
    if data != '':
        print(data)
        if "passe" in data:
            print("Je balance")
            skt.send(b"g1ve_m3_th3_fl4g\n")
