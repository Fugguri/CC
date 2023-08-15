from utils.texts import Texts
from aiogram import Bot, Dispatcher, executor
from config import TOKEN_API, ID_INSTANCE, API_TOKEN_INSTANCE
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from DB.sqlite_connection import Database
from utils.wats import Watsapp
import logging
# from aiogram.contrib.middlewares.logging import LoggingMiddleware
import os
logger = logging.getLogger(__name__)
storage = MemoryStorage()
py_handler = logging.FileHandler(f"logs/{__name__}.log", mode='w')
logger.setLevel(logging.DEBUG)
logger.addHandler(py_handler)


bot = Bot(TOKEN_API, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)
db = Database("CC.db")
wa = Watsapp()
texts = Texts()


async def on_startup(_):
    print("Бот запущен")
    logger.debug("Запущен бот!")
    db.cbdt()


async def on_shutdown(_):
    print("Бот остановлен")


if __name__ == "__main__":
    from handlers import dp
    executor.start_polling(
        dispatcher=dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=False
    )
