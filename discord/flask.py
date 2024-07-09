from flask import Flask, request, jsonify
import requests

TOKEN = ''
CHANNEL_ID = 

app = Flask(__name__)

@app.route('/alert', methods=['POST'])
def alert():
    if request.is_json:
        data = request.get_json()
        message = data.get('message', 'No message')
        print(f'Received alert with message: {message}')
        send_alert_to_discord(message)
        return jsonify({"status": "success", "message": message}), 200
    else:
        return jsonify({"status": "error", "message": "Content-Type must be application/json"}), 400

def send_alert_to_discord(message):
    url = f'https://discord.com/api/v9/channels/{CHANNEL_ID}/messages'
    headers = {
        'Authorization': f'Bot {TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {
        'content': message
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print('Message sent successfully')
    else:
        print(f'Failed to send message: {response.status_code}, {response.text}')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
