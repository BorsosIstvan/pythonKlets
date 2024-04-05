from flask import Flask, render_template, jsonify, request
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get('message', '')
    reversed_message = message[::-1]  # Keer het bericht om
    time.sleep(10)  # Wacht 10 seconden
    return jsonify({'reversed_message': reversed_message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
