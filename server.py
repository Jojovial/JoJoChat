import socket
import threading

class SimpleServer:
    def __init__(self, host='localhost', port=3000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        """Start the server and listen for incoming connections."""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}")

        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                print(f"Connection established with {addr}")
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_handler.start()
        except KeyboardInterrupt:
            print("Server shutting down")
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket):
        """Handle communication with a connected client."""
        with client_socket:
            while True:
                try:
                    msg = client_socket.recv(1024).decode('utf-8')
                    if not msg:
                        print("Client disconnected")
                        break
                    if msg.lower() == 'quit':
                        print("Client requested to quit")
                        break
                    else:
                        print(f"Client: {msg}")
                        response = input("Message: ")
                        client_socket.send(response.encode('utf-8'))
                except (ConnectionResetError, ConnectionAbortedError):
                    print("Connection lost")
                    break
                except Exception as e:
                    print(f"Error: {e}")
                    break

if __name__ == "__main__":
    server = SimpleServer()
    server.start()
