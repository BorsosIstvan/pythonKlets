import socket
import threading

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except Exception as e:
            print(f"Fout bij het ontvangen van bericht: {str(e)}")
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('poci.n-soft.net', 5555))

# Vraag de gebruiker om een gebruikersnaam in te voeren
username = input("Voer je gebruikersnaam in: ")
client_socket.send(username.encode('utf-8'))

# Start een thread om berichten te ontvangen
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Blijf berichten invoeren en verzenden
while True:
    message = input()
    client_socket.send(message.encode('utf-8'))
