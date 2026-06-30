import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💵 Daromad"), KeyboardButton(text="💸 Harajat")],
        [KeyboardButton(text="🏦 Bank"), KeyboardButton(text="💰 Kassa")],
        [KeyboardButton(text="📈 Statistika"), KeyboardButton(text="📊 Hisobot")],
        [KeyboardButton(text="👥 Qarzlar"), KeyboardButton(text="🎯 Jamg'arma")],
        [KeyboardButton(text="⚙️ Sozlamalar")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🏠 Asosiy menyu\n\nQuyidagi bo'limlardan birini tanlang:",
        reply_markup=main_menu
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())