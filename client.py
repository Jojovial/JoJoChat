import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if msg.lower() == 'quit':
                print("Server disconnected")
                break
            else:
                print(f"Server: {msg}")
        except (ConnectionResetError, ConnectionAbortedError):
            print("Connection lost")
            break
        except Exception as e:
            print(f"Error: {e}")
            break
    client_socket.close()

def send_messages(client_socket):
    while True:
        try:
            msg = input("Message: ")
            client_socket.send(msg.encode('utf-8'))
            if msg.lower() == 'quit':
                break
        except (ConnectionResetError, ConnectionAbortedError):
            print("Connection lost")
            break
        except Exception as e:
            print(f"Error: {e}")
            break
    client_socket.close()

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 3000))
    print("Connected to the server")

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))

    receive_thread.start()
    send_thread.start()

    receive_thread.join()
    send_thread.join()
    print("Client disconnected")

if __name__ == "__main__":
    start_client()
