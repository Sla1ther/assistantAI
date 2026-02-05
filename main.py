import os
import threading
from gemini_client import GeminiClient
from bot import TelegramBot
import asyncio
from flask import Flask
 
app = Flask(__name__)
 
@app.route('/')
def home():
    return "OK"
 
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
async def main():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        print("Token not found. Please set the BOT_TOKEN environment variable.", flush=True)

    ai_client = GeminiClient()
    bot = TelegramBot(client=ai_client, token=BOT_TOKEN)
    await bot.start_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    asyncio.run(main())