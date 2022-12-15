import socket

PORT = 1237


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), PORT))
s.listen(5)

player1_socket = None
player2_socket = None

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address}")
    if player1_socket is None:
        player1_socket = clientsocket
        continue
    player2_socket = clientsocket
    break
    # clientsocket.send(bytes("Welcome", "utf-8"))

player1_field = player1_socket.recv(2048).decode()


