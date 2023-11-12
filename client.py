import socket

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def send_message(self, message):
        self.sock.sendall(message.encode())

    def receive_message(self):
        try:
            return self.sock.recv(1024)
        except:
            return None
