import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1237))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address}")
    clientsocket.send(bytes("Welcome", "utf-8"))
