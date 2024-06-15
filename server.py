import socket
import threading

def handle_client(client_socket):
    with client_socket:
        while True:
            try:
                msg = client_socket.recv(1024).decode('utf-8')
                if msg.lower() == 'quit':
                    print("Client disconnected")
                    break
                else:
                    print(f"Client: {msg}")
                    client_socket.send(input("Message: ").encode('utf-8'))
            except (ConnectionResetError, ConnectionAbortedError):
                print("Connection lost")
                break
            except Exception as e:
                print(f"Error: {e}")
                break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 3000))
    server.listen()
    print("Server listening on port 3000")

    try:
        while True:
            client_socket, addr = server.accept()
            print(f"Connection established with {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    except KeyboardInterrupt:
        print("Server shutting down")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
