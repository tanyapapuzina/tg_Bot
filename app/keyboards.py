from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Каталог")],
                                     [KeyboardButton(text="Корзина")],
                                     [KeyboardButton(text="Контакты"),
                                     KeyboardButton(text="О нас")]],
                           resize_keyboard=True,
                           input_field_placeholder="Выбери пункт меню...")

catalog = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Футболки', callback_data='ashot')],
                                [InlineKeyboardButton(text='Кроссы', callback_data='cross')],
                                [InlineKeyboardButton(text='Кепарики', callback_data='cap')],
                                [InlineKeyboardButton(text='Тапки',callback_data='tapki'),
                                 InlineKeyboardButton(text='Головные уборы', callback_data='gol')]])

get_nimber = ReplyKeyboardMarkup(keyboard=
                                 [[KeyboardButton(text='Отправить номер',
                                   request_contact=True)]],
                                 resize_keyboard=True)