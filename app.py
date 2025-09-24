from flask import Flask
import threading
import subprocess
import sys
import os

app = Flask(__name__)

# === Run bot in background thread ===
def run_discord_bot():
    subprocess.run([sys.executable, "bot.py"])

bot_thread = threading.Thread(target=run_discord_bot, daemon=True)
bot_thread.start()

# === Web endpoint for UptimeRobot ===
@app.route('/')
def index():
    return "Bot is running in the background!"

# === Start Flask ===
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
