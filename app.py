from flask import Flask
import subprocess
import threading
import sys

app = Flask(__name__)

def run_discord_bot():
    subprocess.run([sys.executable, "bot.py"])

# Start the Discord bot in a separate thread
bot_thread = threading.Thread(target=run_discord_bot, daemon=True)
bot_thread.start()

@app.route('/')
def index():
    return "Discord bot is running in the background!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)