from gc import callbacks

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_cat, get_items, get_korzina

# pri_start = ReplyKeyboardMarkup(keyboard=[KeyboardButton(text='Проийти регистрацию')],
#                                 resize_keyboard=True)

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Каталог")],
                                     [KeyboardButton(text="Корзина")],
                                     [KeyboardButton(text="Контакты"),
                                     KeyboardButton(text="О нас")]],
                           resize_keyboard=True,
                           input_field_placeholder="Выбери пункт меню...")

get_nimber = ReplyKeyboardMarkup(keyboard=
                                 [[KeyboardButton(text='Отправить номер',
                                   request_contact=True)]],
                                 resize_keyboard=True)

async def catalog():
    all_category = await get_cat()
    keyboard = InlineKeyboardBuilder()
    for category in all_category:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f'category_{category.id}'))
    # keyboard.add(InlineKeyboardButton(text='Корзина', callback_data='Корзина'))
    return keyboard.adjust(2).as_markup()

async def tovarik(id):
    all_items = await get_items(id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f'item_{item.id}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='nazad'))
    return keyboard.adjust(1).as_markup()

async def korzina_nazad():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Добавить в корзину', callback_data='add_korzina'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='nazad'))
    return keyboard.adjust(1).as_markup()

async def nazad():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Удалить из корзины', callback_data='delete'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='nazad'))
    return keyboard.adjust(1).as_markup()

async def reg():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Регистрация', callback_data='reg'))
    return keyboard.adjust(1).as_markup()

async def view_kor(tg_id):
    all_kor = await get_korzina(tg_id)
    keyboard = InlineKeyboardBuilder()
    for tovar in all_kor:
        keyboard.add(InlineKeyboardButton(text=tovar.name, callback_data=f'kor_{tovar.id}'))
    return keyboard.adjust(1).as_markup()
