import discord
import requests
from flask import Flask, request, jsonify
import asyncio

TOKEN = ''
CHANNEL_ID = 

app = Flask(__name__)
client = discord.Client(intents=discord.Intents.default())

@app.route('/alert', methods=['POST'])
def alert():
    if request.is_json:
        data = request.get_json()
        message = data.get('message', 'No message')
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

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('Bot is now connected!')

async def run_bot():
    await client.start(TOKEN)

def run_flask():
    app.run(host='127.0.0.1', port=5432)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    loop.run_until_complete(asyncio.gather(
        asyncio.to_thread(run_flask),
        client.wait_until_ready()
    ))
