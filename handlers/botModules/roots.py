from handlers.controllers.clientControllers import *
from handlers.controllers.states import *
import requests, json
from colorama import Fore, Style
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

async def getTokenList():
    url = "https://uanalytics-api.herokuapp.com/api/v1/token/top?page=0&size=10"
    headers = {
        "Host": "uanalytics-api.herokuapp.com",
        "Origin": "https://ushi.pro",
        "Referer": "https://ushi.pro/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "ru,en;q=0.9,uk;q=0.8,cy;q=0.7",
        "Connection": "close",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        json_data = json.loads(response.text)

        renewedList = []

        for item in json_data["content"][:10]:

            def refactorList():
                tokenData = {
                    "tokenLink": f'https://app.ushi.pro/token/{item["address"]}',
                    "tokenName": item['name'],
                    "symbol": item['symbol'],
                    "price": item['price'],
                    "dayDiff": item['price24hUsdDiff'],
                    "mcap": item['mcap'],
                    "liquidity": item['liquidityUsd'],
                    "dayVolume": item['volume24hUsd'],
                    "holders": item['holders'],
                }
                renewedList.append(tokenData)
                return renewedList
            refactorList()
        
        try:
            sqlite_db.sqlUpdateDay()    
            lastTokenList = sqlite_db.getLastTokenList()
        except:
            pass
        
        def compareLists(prevList, newList):
            newValues = {d['tokenLink'] for d in newList}
            missingValues = [value for value in newValues if value not in prevList]
            return missingValues
        
        difference = compareLists(lastTokenList, renewedList)
        
        if difference:
            
            def findTokenDataByLink(newList, alikeLink):
                for dictionary in newList:
                    if "tokenLink" in dictionary and dictionary["tokenLink"] == alikeLink:
                        return dictionary
            
            try:
                for alikeToke in difference:
                    tokenData = findTokenDataByLink(renewedList, alikeToke)
                    print(Fore.MAGENTA + '[NEW]' + Style.RESET_ALL, end=' ')
                    print(f'Обнаружен новый токен в Hot! – {tokenData["tokenName"]}')
                    await newTokenInfo(mainStates.mainState, tokenData)
                    
            except:
                pass
            
            
            
        sqlite_db.sqlAddTokenData(renewedList)  
        return renewedList   
    else:
        print("Ошибка запроса!")
    


async def mainMenu(
    callback_query: types.CallbackQuery = None,
    message: types.Message = None,
    state: FSMContext = None,
    tokenData=None,
):  
    async def mainMenuBase(entryEntity, state, tokenData):
        await mainStates.mainState.set()
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton(text="♻️ Обновить", callback_data="renewList")
        )

        message_text = ""
        for token in tokenData[:10]:
            tokenMsg = await generateTokenMessage(token)
            message_text += f"{tokenMsg}\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n"

        message_text = await displayingText(message_text)

        try:
            try:
                async with state.proxy() as userData:
                    sendMessage = await bot.edit_message_text(
                        chat_id=userData["mainState"][0],
                        text=message_text,
                        message_id=userData["mainState"][1],
                        reply_markup=keyboard,
                        parse_mode=parse_mode,
                        disable_web_page_preview=True,
                    )
            except Exception as e:
                if str(e)[:23] == "Message is not modified":
                    await callback_query.answer(
                        "Данные еще не изменились, обновите позже."
                    )
                else:
                    sendMessage = await bot.send_message(
                        chat_id=entryEntity.message.chat.id,
                        text=message_text,
                        parse_mode=parse_mode,
                        reply_markup=keyboard,
                        disable_web_page_preview=True,
                    )
                    await state.update_data(
                        mainState=(entryEntity.message.chat.id, sendMessage.message_id)
                    )
        except:
            sendMessage = await bot.send_message(
                chat_id=entryEntity.chat.id,
                text=message_text,
                parse_mode=parse_mode,
                reply_markup=keyboard,
                disable_web_page_preview=True,
            )
            await state.update_data(
                mainState=(entryEntity.chat.id, sendMessage.message_id)
            )

    tokenData = await getTokenList()
    await mainMenuBase(callback_query, state, tokenData)


async def newTokenInfo(users = None, tokenData=None):
    message_text = await generateTokenMessage(tokenData)
    keyboard = await generateTokenButton(tokenData)
    message_text = f'*🥩 Новый токен в Hot!*\n\n{message_text}'
    message_text = await displayingText(message_text)
    
    for user in users:
        try:
            
            await bot.send_message(chat_id=user[0], text=str(message_text), parse_mode=parse_mode, disable_web_page_preview=True, reply_markup=keyboard)
        except Exception as e:
            print('не удалось отправить новый токен', e)