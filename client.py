import socket
import threading

class SimpleClient:
    def __init__(self, host='localhost', port=3000):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        """Start the client and connect to the server."""
        self.client_socket.connect((self.host, self.port))
        print("Connected to the server")

        receive_thread = threading.Thread(target=self.receive_messages)
        send_thread = threading.Thread(target=self.send_messages)

        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()

        print("Client disconnected")

    def receive_messages(self):
        """Receive messages from the server."""
        while True:
            try:
                msg = self.client_socket.recv(1024).decode('utf-8')
                if not msg:
                    break
                if msg.lower() == 'quit':

