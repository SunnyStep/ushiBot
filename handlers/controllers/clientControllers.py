from aiogram import types
from createBot import dp, bot
from aiogram.types import InputMediaPhoto
from aiogram.utils.markdown import link
from database import sqlite_db
from keyboards.keys import createKeyboard
from aiogram.dispatcher import FSMContext
from handlers.controllers.states import *
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

parse_mode = "MarkdownV2"


async def nullFunc(
    callback_query: types.CallbackQuery = None,
    message: types.Message = None,
    state: FSMContext = None,
):
    pass


async def messageText(messageName):
    message_data = await sqlite_db.sqlGetMessageById(messageName)
    message_text = message_data[2] if message_data else None
    return message_text


async def messageImgText(messageName):
    message_data = await sqlite_db.sqlGetMessageById(messageName)
    message_text = message_data[2] if message_data else None
    message_img = sqlite_db.cur.execute(
        "SELECT imgID FROM images WHERE imgName=?", (message_data[3],)
    ).fetchone()
    return message_text, message_img


async def displayingText(text):
    # text = text.replace("\\", "\\\\")
    text = text.replace(".", "\.")
    text = text.replace("-", "\-")
    text = text.replace("!", "\!")
    # text = text.replace("(", "\(")
    # text = text.replace(")", "\)")
    text = text.replace("|", "\|")
    text = text.replace("#", "\#")
    text = text.replace("+", "\+")
    text = text.replace("{", "\{")
    text = text.replace("}", "\}")
    text = text.replace("=", "\=")
    return text


async def imgMessageComp(message_id):
    message_data = await sqlite_db.sqlGetMessageById(message_id)
    message_text = await displayingText(message_data[2])
    try:
        message_img = (await messageImgText(message_id))[1][0]
    except:
        message_img = None
    return message_img, message_text


async def keyboardMessageCompIfExists(message):
    reply_buttons, button_type = await sqlite_db.sqlGetButtonsById(message)
    try:
        keyboard = createKeyboard(reply_buttons, button_type)
    except:
        keyboard = None
    return keyboard


async def generateTokenMessage(tokenData):
    def format_number_with_brackets(number):
        number = float(number)
        formatted_number = "{:.15f}".format(number)
        string_number = str(formatted_number)
        decimal_part = string_number.split(".")[1]  # Получаем десятичную часть числа

        zeros_count = 0
        for digit in decimal_part:
            if digit == "0":
                zeros_count += 1
            else:
                break

        finalNumber = f"0.0\({zeros_count}\){formatted_number[int(zeros_count)+2:][:4]}"
        return finalNumber

    if round(tokenData["dayDiff"]) < 0:
        dayDiff = f'{round(tokenData["dayDiff"])}% 🔻'
    else:
        dayDiff = f'{round(tokenData["dayDiff"])}% ⚡️'

    message_text = f'*[{tokenData["tokenName"]}]({tokenData["tokenLink"]})* | *{tokenData["symbol"]}*\nЦена: *{format_number_with_brackets(tokenData["price"])}*\nРазница/24ч: *{dayDiff}*\nКапа: *{round(int(tokenData["mcap"]))}$*\nЛиквидность: *{round(int(tokenData["liquidity"]))}$*'
    return message_text


async def generateTokenButton(tokenData):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=tokenData['symbol'], url=tokenData['tokenLink']))
    return keyboard
    

# async def messageInfoToArray(currentMessage, messageName):

#     try:
#         if isinstance(currentMessage, types.CallbackQuery):
#             currentMessage = currentMessage.message

#         messageId = currentMessage.message_id
#         chatId = currentMessage.chat.id
#         messageName = messageName
#     except Exception as e:
#         print(e)

#     result = (messageId, chatId, messageName)
#     return result


# async def stepBack(callback_query: types.CallbackQuery, state: FSMContext):

#     async with state.proxy() as messageData:
#         messageHistory = messageData['messageHistory']

#         if not (await state.get_state()) == 'FSMConditions:principles':
#             # if not messageData['messageHistory'][-2][2] == 'workMenu':
#                 await mainStates.currentMessage.set()

#         chatIdDict = {"id": messageHistory[len(messageHistory)-2][1]}
#         chatIdDict = SimpleNamespace(**chatIdDict)

#         entryEntity = {
#             "chat": chatIdDict,
#             "message_id": messageHistory[len(messageHistory)-2][0]
#         }

#         entryEntity = SimpleNamespace(**entryEntity)

#         try:
#             await messageActions('editInlineImg', messageHistory[len(messageHistory)-2][2], entryEntity)
#         except:
#             await messageActions('editInlineText', messageHistory[len(messageHistory)-2][2], entryEntity)

#         await state.update_data(messageHistory=messageData['messageHistory'].pop())


async def messageActions(action, messageData, entryEntity):
    if action == "editInlineImg":
        message_img, message_text = await imgMessageComp(messageData)
        keyboard = await keyboardMessageCompIfExists(messageData)
        result = await bot.edit_message_media(
            chat_id=entryEntity.chat.id,
            media=InputMediaPhoto(
                media=message_img, caption=message_text, parse_mode=parse_mode
            ),
            message_id=entryEntity.message_id,
            reply_markup=keyboard,
        )

    elif action == "sendImg":
        message_img, message_text = await imgMessageComp(messageData)
        keyboard = await keyboardMessageCompIfExists(messageData)
        result = await bot.send_photo(
            chat_id=entryEntity.chat.id,
            photo=message_img,
            caption=message_text,
            parse_mode=parse_mode,
            reply_markup=keyboard,
        )

    elif action == "editInlineText":
        message_img, message_text = await imgMessageComp(messageData)
        keyboard = await keyboardMessageCompIfExists(messageData)
        result = await bot.edit_message_text(
            chat_id=entryEntity.chat.id,
            text=message_text,
            parse_mode=parse_mode,
            message_id=entryEntity.message_id,
            reply_markup=keyboard,
        )

    elif action == "sendText":
        message_img, message_text = await imgMessageComp(messageData)
        keyboard = await keyboardMessageCompIfExists(messageData)
        result = await bot.send_message(
            chat_id=entryEntity.chat.id,
            text=message_text,
            parse_mode=parse_mode,
            reply_markup=keyboard,
        )

    return result


# async def historyPrint(callback_query: types.CallbackQuery = None, message: types.Message = None, state: FSMContext = None):
#     try:
#         async with state.proxy() as data:
#             print(data['messageHistory'])
#         print(f'текущий стейт - {await state.get_state()}')
#     except:
#         print('истории нет')


# async def historyUpdate(currentMessage, messageName, state):
#     currentMessageInfo = await messageInfoToArray(currentMessage, messageName)

#     async with state.proxy() as data:
#         await state.update_data(messageHistory=data['messageHistory'].append(currentMessageInfo))


# async def optionSelectorLite(optionList: None):
#     while (not (len(optionList) % 2) == 0):
#         optionList.append(('filler', '🐍'))

#     keyboard = InlineKeyboardMarkup()

#     for i, option in enumerate(optionList):
#         y = i + 2
#         if (y % 2 == 0):
#             keyboard.add(InlineKeyboardButton(
#                 text=option[1], callback_data=option[0]))
#         else:
#             keyboard.insert(InlineKeyboardButton(
#                 text=option[1], callback_data=option[0]))

#     return keyboard


# async def optionSelector(optionList: None, callback_query: None, state: None):
#     if callback_query.data in ('nextPage', 'prevPage'):
#         try:
#             async with state.proxy() as pageData:
#                 pageNum = pageData['pageNum']
#             if callback_query.data == 'nextPage':
#                 newPageNum = pageNum+1
#             else:
#                 newPageNum = pageNum-1

#             await state.update_data(pageNum=newPageNum)
#             p = (newPageNum - 1)*6

#         except Exception as e:
#             print(e)

#     else:
#         newPageNum = 1
#         await state.update_data(pageNum=newPageNum)
#         p = 0

#     pageCount = math.ceil(len(optionList) / 6)

#     while (not (len(optionList) % 6) == 0):
#         optionList.append(('filler', ' '))

#     keyboard = InlineKeyboardMarkup()

#     for i, option in enumerate(optionList[p:(p+6)]):
#         y = i * 3 + 2
#         if (y % 2 == 0):
#             keyboard.add(InlineKeyboardButton(
#                 text=option[1], callback_data=option[0]))
#         else:
#             keyboard.insert(InlineKeyboardButton(
#                 text=option[1], callback_data=option[0]))

#     if newPageNum == 1:
#         keyboard.add(InlineKeyboardButton(
#             text='◀️ Назад', callback_data='back'))
#         keyboard.insert(InlineKeyboardButton(
#             text='▶️', callback_data='nextPage'))
#     elif newPageNum == pageCount:
#         keyboard.add(InlineKeyboardButton(text='◀️', callback_data='prevPage'))
#         keyboard.insert(InlineKeyboardButton(text='🐍', callback_data='filler'))
#     else:
#         keyboard.add(InlineKeyboardButton(text='◀️', callback_data='prevPage'))
#         keyboard.insert(InlineKeyboardButton(
#             text='▶️', callback_data='nextPage'))

#     return keyboard
