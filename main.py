import os
from gemini_client import GeminiClient
from bot import TelegramBot
import asyncio
async def main():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        print("Token not found. Please set the BOT_TOKEN environment variable.")

    ai_client = GeminiClient()
    bot = TelegramBot(cl=ai_client, token=BOT_TOKEN)
    await bot.start_polling()

if __name__ == "__main__":
    asyncio.run(main())