from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from keyboards.keyboards import schoise_kb, posts_menu_kb

from main import dp, bot, db, wa, texts

from utils.exel import exel_reader
from DB.sqlite_connection import Texts
db_texts = Texts("CC.db")
cur_cad_num = ""


class Posts(StatesGroup):
    post_action = State()
    edit_post_text = State()
    new_post_text = State()
    new_post = State()
    new_post_comment = State()
    new_post_messanger = State()
    confirm_new_post = State()
    confirm_update_text = State()


new_post_name = ""
new_post_text = ""
new_comment_for_programmer = ""
current_post = ""
new_post_messanger = ""


@dp.message_handler(Text("Посты"), state="*")
async def posts_menu(message: types.Message):
    markup = await posts_menu_kb()
    await message.answer("Выберите пункт меню", reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data == "post registry", state="*")
async def post_registry(callback: types.CallbackQuery, state=State):
    text = "<b>Реест постов</b>\n"
    posts = db_texts.get_all_texts()
    for data in posts:
        text += '10{}({})\n{}\n\n'.format(
            data[0], data[3], data[1])
    await callback.message.answer(text)
    await state.finish()


@dp.callback_query_handler(lambda call: call.data == "new post", state="*")
async def new_post(callback: types.CallbackQuery):
    text = """<b>Введите код-номер поста, который хотите отредактировать или введите 000 чтобы добавить новый пост.</b>"""
    await callback.message.answer(text)
    print(callback.message.text)
    await Posts.post_action.set()


@dp.message_handler(state=Posts.post_action)
async def post_action(message: types.Message, state: State):
    if message.text == "000":
        await Posts.new_post_text.set()
        await message.answer(f"Введите текст нового поста")
        return
    global current_post
    current_post = message.text[2:]
    try:
        text = db_texts.get_text_by_id(current_post)
        await message.answer(f"Текущий текст:\n{text}\n\nВведите текст для поста - {current_post}")
        await Posts.edit_post_text.set()
    except:
        await message.answer(f"Нет поста с кодом - {message.text}.\nПроверьте данные и попробуйте снова")


@dp.message_handler(state=Posts.new_post_text)
async def edit_post(message: types.Message):
    global new_post_text
    new_post_text = message.text
    await message.answer(f"Введите комментарий для программиста \n")
    await Posts.new_post_comment.set()


@dp.message_handler(state=Posts.new_post_comment)
async def edit_post(message: types.Message):
    global new_comment_for_programmer
    new_comment_for_programmer = message.text
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Whatsapp", callback_data="whatsapp"),
               types.InlineKeyboardButton(
                   text="Telegram", callback_data="telegram")
               )
    await message.answer("Выберите мессенджер", reply_markup=markup)
    await Posts.new_post_messanger.set()


@dp.callback_query_handler(state=Posts.new_post_messanger)
async def edit_post(callback: types.CallbackQuery, state: State):
    markup = await schoise_kb()
    global new_post_messanger
    new_post_messanger = callback.data
    await callback.message.answer(f"{current_post}({new_post_messanger})\n{new_post_text}", reply_markup=markup)
    await Posts.confirm_new_post.set()


@dp.callback_query_handler(state=Posts.confirm_new_post)
async def confim_new_post(callback: types.CallbackQuery, state: State):
    if callback.data == "yes":
        db_texts.set_new_text(
            new_post_text, new_comment_for_programmer, new_post_messanger)
        await callback.message.answer(f"Создан новый пост")
        await state.finish()
    else:
        await new_post(callback)


@dp.message_handler(state=Posts.edit_post_text)
async def edit_post(message: types.Message, state: State):
    global new_post_text
    new_post_text = message.text
    markup = await schoise_kb()
    messanger = db_texts.get_text_by_id(current_post)[3]
    await message.answer(f"{current_post}({messanger})\n{new_post_text}", reply_markup=markup)
    await Posts.confirm_update_text.set()


@dp.callback_query_handler(state=Posts.confirm_update_text)
async def confim_edit_post(callback: types.CallbackQuery, state: State):
    if callback.data == "yes":
        db_texts.update_col_data("text",
                                 new_post_text, current_post)
        await callback.message.answer('Пост № {} Обновлен. \nНовый текст: {}'.format(current_post, new_post_text))
        await state.finish()
    else:
        await new_post(callback)


def register_posts():
    dp.register_callback_query_handler()
    dp.register_message_handler()
