from aiogram import types
from main import dp, bot
from aiogram.dispatcher.filters.state import State
from keyboards.keyboards import start_kb


@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message):
    markup = await start_kb()

    await message.answer("Добро пожаловать. Выберите пункт меню, который вас интересует.", reply_markup=markup)
