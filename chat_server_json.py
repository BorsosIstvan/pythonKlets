import socket
import threading
import json
from datetime import datetime
import signal
import sys


def read_chat_history():
    chat_history = []

    try:
        with open('chat.json', 'r') as file:
            for line in file:
                entry = json.loads(line)
                chat_history.append(entry)
    except FileNotFoundError:
        print("Chatgeschiedenisbestand niet gevonden.")
    except json.JSONDecodeError as e:
        print(f"Fout bij het decoderen van JSON: {str(e)}")

    return chat_history


def save_message_to_json(username, message):
    timestamp = str(datetime.now())
    entry = {'timestamp': timestamp, 'username': username, 'message': message}

    with open('chat.json', 'a') as file:
        json.dump(entry, file)
        file.write('\n')


def handle_client(client_socket, username):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"{username}: {message}")

            save_message_to_json(username, message)

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


def stop_server(signum, frame):
    print("\nServer gestopt.")
    server.close()
    sys.exit(0)


def start_server():
    signal.signal(signal.SIGINT, stop_server)

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
