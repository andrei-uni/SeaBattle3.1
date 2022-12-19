import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1237))
s.listen(5)

player1_socket, _ = s.accept()
player1_field = player1_socket.recv(512)

player2_socket, _ = s.accept()
player2_field = player2_socket.recv(512)

player1_socket.send(player2_field)
player2_socket.send(player1_field)

player1_turn = True


def did_hit(data: bytes) -> bool:
    return data.decode() == "HIT"


while True:
    while player1_turn:
        coords = player1_socket.recv(512)
        player2_socket.send(coords)
        res = player1_socket.recv(512)
        if not did_hit(res):
            player1_turn = False

    while not player1_turn:
        coords = player2_socket.recv(512)
        player1_socket.send(coords)
        res = player2_socket.recv(512)
        if not did_hit(res):
            player1_turn = True
