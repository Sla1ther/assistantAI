import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, BufferedInputFile
from aiogram.filters import Command
import threading

class TelegramBot:
    def __init__(self, client, token):
        
        self.cl = client
        self.token = token
        self.router = Router()
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.history = []
        self.scrPassword = "1234"

        self.handlersSetup()
        self.dp.include_router(self.router)
    
    def handlersSetup(self):
        @self.router.message(Command("start"))
        async def startCmd(message):
            await message.answer(
                "Привіт!\n"
                "Я ШІ.\n"
                f"Ви вибрали режим: {self.cl.current_mode}\n"
                "Напишіть мені щось, і я відповім вам АБО обирай режим\n",
                reply_markup=self.botKeyboard()
            )
            print(f"New user started TG bot: {message.from_user.id}")
        
        @self.router.message(lambda m: m.text == "Default" or m.text == "Programmer")
        async def ModeChange(message: Message):
            if message.text == "Default":
                self.cl.setMode("default")
                await message.answer("Режим змінено на Default")
                print(f"User {message.from_user.id} changed mode to Default")
            elif message.text == "Programmer":
                self.cl.setMode("programmer")
                await message.answer("Режим змінено на Programmer")
                print(f"User {message.from_user.id} changed mode to Programmer")

        @self.router.message(lambda m: m.text == "History")
        async def history(message: Message):
            if self.history:
                history_text = "\n".join([f" You: {me}\n AI: {ai}" for me, ai in self.history])
                await message.answer(f"Історія повідомлень:\n{history_text}")
            else:
                await message.answer("Історія порожня.")

        
        @self.router.message()
        async def aiChat(message: Message):
            if message.text.startswith('/'):
                return
            print(f"Отримано {message.text[:50]}")
            await message.answer("Думаю...")
            
            response = self.cl.ask(message.text)
            max_len = 4000
            for i in range(0, len(response), max_len):
                await message.answer(response[i:i+max_len])
            self.history.append((message.text, response))
            if len(self.history) > 3:
                self.history.pop(0)
    
    def botKeyboard(self):
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Default'), KeyboardButton(text='Programmer')],
                [KeyboardButton(text='History'), KeyboardButton(text='/screenshot')]
            ],
            resize_keyboard=True,
        )
    
    

    def runBot(self):
        async def main():
            print("🤖 Telegram Bot запущено")
            await self.dp.start_polling(self.bot)
       
        asyncio.run(main())
   
    def start(self):
        self.botThread.start()

    async def start_polling(self):
        await self.dp.start_polling(self.bot)


