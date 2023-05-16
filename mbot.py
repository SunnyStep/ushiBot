# -*- coding: utf-8 -*-

from aiogram.utils import executor
from createBot import dp
from handlers.client import sqlite_db
import logging
from colorama import Fore, Style 


async def on_startup(_):
    print(Fore.GREEN + '[OK]' + Style.RESET_ALL, end=' ')
    print('Бот запущен.')
    sqlite_db.sql_start()
    

from handlers import client
from handlers.controllers import messageHandlers

messageHandlers.register_handlers_client(dp)

logging.getLogger('aiogram').setLevel(logging.ERROR)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
