from aiogram import types, Dispatcher
from createBot import dp, bot
from aiogram.types import InputMediaPhoto
from aiogram.dispatcher import FSMContext
from database import sqlite_db
import datetime
from handlers.botModules import roots


parse_mode = "MarkdownV2"


async def botStart(message: types.Message, state: FSMContext):
    user_exists = await sqlite_db.sqlCheckUser(message.from_user.id)

    if user_exists:
        await roots.mainMenu(None, message, state)
    else:
        print('Неизвестный вход')
