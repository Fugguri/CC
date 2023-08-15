from aiogram import Bot, types
from config import TOKEN_API, admin_telegram_id, developer_telegram_id
from .texts import Texts
from .utils import Utils
import asyncio


class Telegram(Utils):
    def __init__(self) -> None:
        self.bot = Bot(TOKEN_API, parse_mode="HTML")
        self.admin_telegram_id = admin_telegram_id
        self.developer_telegram_id = developer_telegram_id
        self.create_text = Texts()

    def new_form_notification(self, text, media=None):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            text="Добавить пользователя", callback_data="add_from_form"))
        markup.add(types.InlineKeyboardButton(
            text="Отклонить", callback_data="cancel_from_form"))

        if not media:
            asyncio.run(self.bot.send_message(
                        chat_id=self.developer_telegram_id, text=text, reply_markup=markup))

            asyncio.run(self.bot.send_message(
                chat_id=self.admin_telegram_id, text=text))

    def send_telegram_notification(self, text, media=None):

        if not media:
            asyncio.run(self.bot.send_message(
                        chat_id=self.developer_telegram_id, text=text))

            asyncio.run(self.bot.send_message(
                chat_id=self.admin_telegram_id, text=text))
            
        else:

            media_group = types.MediaGroup()
            for media in media:
                media_group.attach_photo(types.InputFile(media), 'Фото')

            asyncio.run(self.bot.send_media_group(
                chat_id=self.developer_telegram_id, media=media_group))

            asyncio.run(self.bot.send_message(
                        chat_id=self.developer_telegram_id, text=text))

            asyncio.run(self.bot.send_media_group(
                chat_id=self.admin_telegram_id, media=media_group))
            
            asyncio.run(self.bot.send_message(
                        chat_id=self.admin_telegram_id, text=text))
