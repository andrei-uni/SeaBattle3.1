import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1237))
s.listen(5)

player1_socket, address = s.accept()
print(f"Connection from {address}")
player1_field = player1_socket.recv(2048)
print(f"player1Field {player1_field.decode()}")

player2_socket, address = s.accept()
print(f"Connection from {address}")
player2_field = player2_socket.recv(2048)
print(f"player2Field {player2_field.decode()}")

player1_socket.send(player2_field)
player2_socket.send(player1_field)

player1_turn = True

# while True:
#     if player1_turn:

