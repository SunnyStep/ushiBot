from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Tuple, Union


def createKeyboard(reply_buttons: List[Tuple[str, str]], buttonType: str) -> Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]:
    
    if buttonType == 0:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        y = 1
        for button in reply_buttons:
            y += 1
            if (y % 2 == 0):
                keyboard.add(button[0])
            else:
                keyboard.insert(button[0])
    
    else:
        keyboard = InlineKeyboardMarkup()
        y = 1
        for button in reply_buttons:
            if button[2] == 2:
                y += 1
                if (y % 2 == 0):
                    keyboard.add(InlineKeyboardButton(text=button[0], url=button[3]))
                else:
                    keyboard.insert(InlineKeyboardButton(text=button[0], url=button[3]))
            else:
                y += 1
                if (y % 2 == 0):
                    keyboard.add(InlineKeyboardButton(text=button[0], callback_data=button[1]))
                else:
                    keyboard.insert(InlineKeyboardButton(text=button[0], callback_data=button[1]))
                
    return keyboard
