from flask import Flask, render_template, jsonify
import time

app = Flask(__name__)

# Route voor de indexpagina
@app.route('/')
def index():
    return render_template('index.html')

# Route om elke 30 seconden een bericht te verzenden
@app.route('/message')
def send_message():
    # Stuur een tijdelijke bericht
    message = "Dit is een testbericht van de server."
    return jsonify({'message': message})

@app.route('/send_message', methods=['POST'])
def resend_message():
    data = request.get_json()
    message = data.get('message', '')
    reversed_message = message[::-1]  # Keer het bericht om
    time.sleep(10)  # Wacht 10 seconden
    return jsonify({'reversed_message': reversed_message})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
