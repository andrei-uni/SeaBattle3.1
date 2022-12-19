import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1237))
s.listen(5)

player1_socket, address = s.accept()
print(f"Connection from {address}")
player1_field = player1_socket.recv(2048)

player2_socket, address = s.accept()
print(f"Connection from {address}")
player2_field = player2_socket.recv(2048)

player1_socket.send(player2_field)
player2_socket.send(player1_field)

player1_turn = True


def did_hit(data: bytes) -> bool:
    return data.decode() == "HIT"


while True:
    while player1_turn:
        coords = player1_socket.recv(2048)
        player2_socket.send(coords)
        res = player1_socket.recv(2048)
        if not did_hit(res):
            player1_turn = False

    while not player1_turn:
        coords = player2_socket.recv(2048)
        player1_socket.send(coords)
        res = player2_socket.recv(2048)
        if not did_hit(res):
            player1_turn = True
