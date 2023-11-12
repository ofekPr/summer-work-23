import socket
import select

class Server:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen(5)
        print("Server started! Waiting for connections...")

        self.clients = []
        self.usernames = {}

    def handle_clients(self):
        while True:
            readable, _, _ = select.select([self.sock] + self.clients, [], [])
            for s in readable:
                if s is self.sock:
                    client_sock, client_address = self.sock.accept()
                    print(f"Accepted connection from {client_address}")
                    username_message = client_sock.recv(1024).decode()
                    username = username_message.split(":")[1].strip()
                    self.usernames[client_sock] = username
                    self.clients.append(client_sock)
                    for client in self.clients:
                        client.send(f"Admin: {username} has joined the chat!".encode())
                else:
                    message = s.recv(1024).decode()
                    if not message:
                        username = self.usernames[s]
                        print(f"{username} has disconnected.")
                        self.clients.remove(s)
                        del self.usernames[s]
                        for client in self.clients:
                            client.send(f"Admin: {username} has left the chat.".encode())
                        continue

                    username = self.usernames[s]
                    for client in self.clients:
                        if client != s:
                            client.send(f"{username}: {message}".encode())

if __name__ == '__main__':
    server = Server('localhost', 12345)
    server.handle_clients()
