import socket


class Network:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip):
        self.s.connect((ip, 1237))

    def send_my_field(self, field: str):
        self.s.send(str.encode(field))

    def get_opponent_field(self) -> str:
        return self.s.recv(2048).decode()

    def send(self, data: str) -> str:
        try:
            self.s.send(str.encode(data))
            reply = self.s.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)
