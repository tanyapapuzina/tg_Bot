from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_cat, get_items

# pri_start = ReplyKeyboardMarkup(keyboard=[KeyboardButton(text='Проийти регистрацию')],
#                                 resize_keyboard=True)

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Проийти регистрацию')],
                                     [KeyboardButton(text="Каталог")],
                                     [KeyboardButton(text="Корзина")],
                                     [KeyboardButton(text="Контакты"),
                                     KeyboardButton(text="О нас")]],
                           resize_keyboard=True,
                           input_field_placeholder="Выбери пункт меню...")

# catalog = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Футболки', callback_data='ashot')],
#                                 [InlineKeyboardButton(text='Кроссы', callback_data='cross')],
#                                 [InlineKeyboardButton(text='Кепарики', callback_data='cap')],
#                                 [InlineKeyboardButton(text='Тапки',callback_data='tapki'),
#                                  InlineKeyboardButton(text='Аксессуары', callback_data='gol')]])
get_nimber = ReplyKeyboardMarkup(keyboard=
                                 [[KeyboardButton(text='Отправить номер',
                                   request_contact=True)]],
                                 resize_keyboard=True)

async def catalog():
    all_category = await get_cat()
    keyboard = InlineKeyboardBuilder()
    for category in all_category:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f'category_{category.id}'))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='menu'))
    return keyboard.adjust(2).as_markup()

async def tovarik(id):
    all_tovar = await get_items(id)
    keyboard = InlineKeyboardBuilder()
    for tovar in all_tovar:
        keyboard.add(InlineKeyboardButton(text=tovar.name, callback_data=f'tovar_{tovar.id}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='nazad'))
    return keyboard.adjust(1).as_markup()

async def nazad():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Назад1', callback_data='nazad1'))
    return keyboard.adjust(1).as_markup()

