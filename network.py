import socket

from Coord import Coord
from GameField import GameField


class Network:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip):
        self.s.connect((ip, 1237))

    def send_my_field(self, field: str):
        self.s.send(str.encode(field))

    def get_opponent_field(self) -> GameField:
        return GameField.convert_to_gamefield(self.s.recv(2048).decode())

    def send_hit_ship(self, did_hit_ship: bool):
        self.s.send(str.encode("HIT" if did_hit_ship else "MISS"))

    def send_move_coord(self, coord: Coord):
        self.s.send(str.encode(f"{coord.row},{coord.column}"))

    def receive_move_coord(self) -> Coord:
        data = self.s.recv(2048).decode().split(",")
        r = int(data[0])
        c = int(data[1])
        return Coord(r, c)