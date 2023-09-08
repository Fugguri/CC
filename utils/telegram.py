from aiogram import Bot, types
from config import TOKEN_API, admin_telegram_id, developer_telegram_id
from .texts import Texts
from .utils import Utils
import asyncio
import os

class Telegram(Utils):
    def __init__(self) -> None:
        from main import bot
        self.bot = bot
        self.admin_telegram_id = admin_telegram_id
        self.developer_telegram_id = developer_telegram_id
        self.create_text = Texts()

    def new_form_notification(self, text, media=None):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            text="Добавить жителя", callback_data="add_from_form"))
        markup.add(types.InlineKeyboardButton(
            text="Отклонить", callback_data="cancel_from_form"))

        if not media:
            asyncio.run(self.bot.send_message(
                        chat_id=self.developer_telegram_id, text=text, reply_markup=markup))

            asyncio.run(self.bot.send_message(
                        chat_id=self.admin_telegram_id, text=text, reply_markup=markup))

    def send_telegram_notification(self, text, media=None):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            text="Ответить", callback_data="answer_request"))
        markup.add(types.InlineKeyboardButton(
            text="Отклонить", callback_data="cancel_request"))
        media_group = types.MediaGroup()
        
        if media:
            if len(media) == 1:
                asyncio.run(self.bot.send_photo(photo=media[0],
                        chat_id=self.developer_telegram_id, caption=text,reply_markup=markup))

                # asyncio.run(self.bot.send_photo(photo=media[0],
                #         chat_id=self.admin_telegram_id, caption=text,reply_markup=markup))
                return
            else:
                for media_item in media:
                    # media_file = open(media_item, "rb") 
                    media_group.attach_photo(types.InputMediaPhoto(media_item), 'Фото')
                    # media_file.close()
                    # os.system(f"rm {media_item}")
                
                asyncio.run(self.bot.send_media_group(
                    chat_id=self.developer_telegram_id, media=media_group))
                asyncio.run(self.bot.send_message(
                                chat_id=self.developer_telegram_id, text=text,reply_markup=markup))

                # asyncio.run(self.bot.send_media_group(
                #     chat_id=self.admin_telegram_id, media=media_group))
                # asyncio.run(self.bot.send_message(
                #         chat_id=self.admin_telegram_id, text=text,reply_markup=markup))
                return
        asyncio.run(self.bot.send_message(
                                chat_id=self.developer_telegram_id, text=text,reply_markup=markup))
        # asyncio.run(self.bot.send_message(
        #         chat_id=self.admin_telegram_id, text=text,reply_markup=markup))