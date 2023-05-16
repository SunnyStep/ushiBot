from aiogram import types, Dispatcher
from handlers.controllers.clientControllers import *
from handlers.controllers.states import *
from handlers.botModules import roots

def register_handlers_client(dp: Dispatcher):
    
    dp.register_message_handler(roots.mainMenu, lambda message: message.text == '/start', state='*')

    # dp.register_message_handler(nullFunc, state='*')
    
    dp.register_callback_query_handler(roots.mainMenu, lambda callback_query: callback_query.data == 'renewList', state=mainStates.mainState)
