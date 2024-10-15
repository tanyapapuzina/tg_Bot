import asyncio

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

import app.keyboards as kb
import app.sost as sos
from app.database.requests import get_opis, add_us, get_items
from app.keyboards import catalog, tovarik, nazad
from aiogram import types
router=Router()

@router.message(CommandStart())
async def start(message:Message):
    await message.answer("Добро пожаловать в супер мега крутой тг магазик!",  reply_markup=kb.main)
    await asyncio.sleep(1)



@router.message(Command("help"))
async def help(message:Message):
    await message.reply("pipi")

@router.message(F.text=="Каталог")
async def cat(message:Message):
    await message.answer("Выбери категорию товара:", reply_markup=await catalog())


@router.callback_query(F.data.startswith('category_'))
async def categor(callback:CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.edit_text(f'Выберите товар:', reply_markup=await tovarik(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('tovar_'))
async def opis(callback:CallbackQuery):
    opi=await get_opis(callback.data.split('_')[1])
    await callback.message.edit_text(f'Название:{opi.name}\nОписание:{opi.description}\nЦена:{opi.price}',
                                  reply_markup=await nazad())

@router.callback_query(F.data.startswith('nazad1'))
async def naza(callback: CallbackQuery):
    tovari = await get_items(callback.data.split('_')[1])
    await callback.answer('Вы выбрали категорию')
    await callback.message.edit_text(f'Выберите товар:', reply_markup=await tovarik(tovari.split('_')[1]))

# @router.callback_query(F.data.startswith('nazad'))
# async def naza(callback:CallbackQuery):
#
#     await callback.message.edit_text(f'Выберите товар:', reply_markup=await catalog())

@router.message(Command('registr'))
async def registr(message:Message, state:FSMContext):
    await state.set_state(sos.Register.name)
    await message.answer('Введите ваше имя')


@router.message(sos.Register.name)
async def registr_name(message:Message, state:FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(sos.Register.famil)
    await message.answer('Введите вашу фамилию')

@router.message(sos.Register.famil)
async def registr_famil(message:Message, state:FSMContext):
    await state.update_data(famil=message.text)
    await state.set_state(sos.Register.age)
    await message.answer('Введите ваш возраст')

@router.message(sos.Register.age)
async def registr_age(message:Message, state:FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(sos.Register.nimber)
    await message.answer('Введите ваш номер', reply_markup=kb.get_nimber)

@router.message(sos.Register.nimber)
async def registr_nimber(message:Message, state:FSMContext):
    if message.contact:
        nimber=message.contact.phone_number
        await state.update_data(nimber=nimber)
    elif message.text:
        nimber=message.text
        await state.update_data(nimber=nimber)
    else:
        await message.answer("Пожалуйста, отправьте контакт или введите правильный номер телефона.")
        return

    data=await state.get_data()
    await message.answer(f'Имя:{data["name"]}\nФамилия:{data["famil"]}\nВозраст:{data["age"]}\nНомер:{data["nimber"]}')
    await state.clear()
    await add_us(message.from_user.id, data['name'], data['famil'], data['age'],data['nimber'])