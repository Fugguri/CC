from aiogram import types
from main import dp, bot
from aiogram.dispatcher.filters.state import State
from keyboards.keyboards import start_kb
from main import db


@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message):
    markup = await start_kb()

    await message.answer("""Это бот-помощник секретаря общих собраний. Он может:
🚀 загрузить данные по помещениям и собственникам
🤳 занести контактные данные жильцов и анкеты собственников
🤖 отправлять сообщения в WhatsApp (виртуальный консьерж дома)
💬 принимать сообщения гостей и жильцов через консьержа дома
📢 информировать всех жильцов об общих собраниях в доме
✅ получать от собственников бюллетени для голосования""", reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data == "cancel_from_form")
async def decline_new_form_user(callback: types.CallbackQuery):
    await callback.message.answer("Отклонено")


@dp.callback_query_handler(lambda call: call.data == "add_from_form")
async def accept_new_form_user(callback: types.CallbackQuery):
    try:
        await callback.message.answer("")
    except Exception as ex:
        await callback.message.answer(ex)
