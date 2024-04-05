from flask import Flask, render_template
from flask_socketio import SocketIO
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading", logger=True, engineio_logger=True, async_handlers=True)

# Indexpagina
@app.route('/')
def index():
    return render_template('index.html')

# Functie voor het periodiek verzenden van berichten naar de client
def send_messages():
    count = 0
    while True:
        socketio.emit('server_message', {'message': f"Dit is bericht {count}"})
        count += 1
        time.sleep(10)  # Wacht 10 seconden tussen elk bericht

# Start het verzenden van berichten wanneer de server wordt gestart
@socketio.on('connect')
def handle_connect():
    send_messages()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000)
