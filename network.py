import socket
from server import PORT


class Network:
    def __init__(self, ip: str):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (ip, PORT)

    def connect(self):
        self.s.connect(self.addr)

    def get_opponent_field(self) -> str:
        return self.s.recv(2048).decode()

    def send_my_field(self, field: str):
        self.s.send(bytes(field))

    def send(self, data: str) -> str:
        try:
            self.s.send(bytes(data))
            reply = self.s.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)
