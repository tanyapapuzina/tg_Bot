from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


class Register(StatesGroup):
    name=State()
    famil=State()
    age=State()
    nimber=State()

class CatalogState(StatesGroup):
    choose_category = State()
    choose_item = State()
    view_item = State()
    view_korzina = State()