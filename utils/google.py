import asyncio
import gspread

from models import User_from_googlesheet
from aiogram import Bot, types
from .telegram import Telegram
from .utils import Utils
from .texts import Texts
from models import User_from_googlesheet
from config import TOKEN_API, gs_filename, gs_form_sheetname


class GoogleSheest(Utils):
    def __init__(self) -> None:
        self.gc = gspread.service_account(gs_filename)
        self.sh = self.gc.open(gs_form_sheetname)
        self.tg = Telegram()
        self.create_text = Texts()

    def collect_guest_data(self):
        worksheet = self.sh.get_worksheet(0)

        cells = worksheet.get_values()
        result = []
        for cell in cells:
            print(cell)
            user = User_from_googlesheet(*cell)
            user.phone = self._convert_number(user.phone)
            result.append(user)

        return result[1:]

    def new_form_notify(self, phone):
        users_from_form = self.collect_guest_data()
        for user in users_from_form:
            if user.phone == phone:
                text = self.create_text.new_user_from_form(user)
                self.tg.new_form_notification(text)
                return
