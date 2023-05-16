from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class mainStates(StatesGroup):
    mainState = State()