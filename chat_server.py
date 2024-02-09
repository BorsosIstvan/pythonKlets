import socket
import threading


def handle_client(client_socket, username):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"{username}: {message}")
            broadcast(f"{username}: {message}", client_socket)
        except Exception as e:
            print(f"Fout bij het ontvangen van bericht van {username}: {str(e)}")
            break

    print(f"{username} heeft de chat verlaten.")
    clients.remove((username, client_socket))
    client_socket.close()


def broadcast(message, sender_socket):
    for (username, client_socket) in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Fout bij het verzenden van bericht naar {username}: {str(e)}")
                clients.remove((username, client_socket))
                client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen(5)
    print("Chatserver luistert op poort 5555...")

    while True:
        client_socket, addr = server.accept()
        print(f"Verbonden met {addr}")

        username = client_socket.recv(1024).decode('utf-8')
        print(f"{username} is toegetreden tot de chat.")

        clients.append((username, client_socket))



        client_handler = threading.Thread(target=handle_client, args=(client_socket, username))
        client_handler.start()


if __name__ == "__main__":
    clients = []
    start_server()
