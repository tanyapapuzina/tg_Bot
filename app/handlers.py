import asyncio
from turtledemo.sorting_animate import show_text

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from pyexpat.errors import messages
from unicodedata import category

import app.keyboards as kb
import app.sost as sos
from app.database.requests import get_opis, add_us, get_items,del_korzina, add_korzina, get_korzina, get_us, get_cat, get_kor
from app.keyboards import catalog, tovarik, korzina_nazad, view_kor, nazad, reg

router=Router()

@router.message(CommandStart())
async def start(message:Message):
    await message.answer("Добро пожаловать! Одежда, обувь и аксессуары для мужчин, женщин и детей.",
                         reply_markup=kb.main)

    tg_id_us = message.from_user.id
    us = await get_us(tg_id_us)
    if not us:
        await message.answer("Для регистрации нажмите на кнопку", reply_markup= await reg())
    else:
        await message.answer("Вы уже зарегистрированы.")
    #await asyncio.sleep(1)

@router.callback_query(F.data.startswith("reg"))
async def registr(callback:CallbackQuery, state:FSMContext):
    tg_id_us = callback.from_user.id
    us = await get_us(tg_id_us)
    if not us:
        await state.set_state(sos.Register.name)
        await callback.message.answer('Введите ваше имя')
    else:
        await callback.message.answer("Вы уже зарегистрированы.")


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
    await message.answer("Спасибо за регестрацию!",
                         reply_markup=kb.main)

@router.message(Command("help"))
async def help(message:Message):
    await message.reply("pipi")

@router.message(F.text=="Каталог")
async def cat(message:Message, state:FSMContext):
    await message.answer("Выбери категорию товара:", reply_markup=await catalog())
    await state.set_state(sos.CatalogState.choose_category)


@router.callback_query(F.data.startswith('category_'))
async def categor(callback:CallbackQuery, state:FSMContext):
    category_id = callback.data.split('_')[1]
    await state.update_data(category_id=category_id)
    await callback.message.edit_text(f'Выберите товар:', reply_markup=await tovarik(category_id))
    await state.set_state(sos.CatalogState.choose_item)

@router.callback_query(F.data.startswith('item_'))
async def opis(callback:CallbackQuery, state:FSMContext):
    opi=await get_opis(callback.data.split('_')[1])
    await callback.message.edit_text(f'Название:{opi.name}\nОписание:{opi.description}\nЦена:{opi.price}',
                                  reply_markup=await korzina_nazad())
    await state.set_state(sos.CatalogState.view_item)
    await state.update_data(id_items_k=opi.id, name_k=opi.name, description_k=opi.description, price_k=opi.price)

@router.callback_query(F.data=='nazad')
async def back(callback:CallbackQuery, state:FSMContext):
    now_sost = await state.get_state()

    data = await state.get_data()
    category_id = data.get('category_id')
    kor_id_items = data.get('kor_id_items')
    if now_sost == sos.CatalogState.view_item:
        await callback.message.edit_text(f'Выберите товар:', reply_markup=await tovarik(category_id))
        await state.set_state(sos.CatalogState.choose_item)

    elif now_sost == sos.CatalogState.choose_item:
        await callback.message.edit_text("Выбери категорию товара:", reply_markup=await catalog())
        await state.set_state(sos.CatalogState.choose_category)

    elif now_sost == sos.CatalogState.view_korzina:
        tg_id = callback.from_user.id
        await callback.message.edit_text("Товары в вашей корзине:", reply_markup=await view_kor(tg_id))

@router.callback_query(F.data=='add_korzina')
async def korzina(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    name_k = data.get('name_k')
    description_k = data.get('description_k')
    price_k = data.get('price_k')
    id_items_k = data.get('id_items_k')
    tg_id_us = callback.from_user.id

    us = await get_us(tg_id_us)
    if us:
        await callback.answer(f'Вы добавили товар {name_k} в корзину')
        await add_korzina(id_items_k, tg_id_us, name_k, description_k, price_k)
    else:
        await callback.message.edit_text('Чтобы добавить товар, пройдите регистрацию!',
                                      reply_markup=await reg())

@router.message(F.text=="Корзина")
async def view_korzina(message:Message):
    tg_id = message.from_user.id
    await message.answer("Товары в вашей корзине:", reply_markup=await view_kor(tg_id))

@router.callback_query(F.data.startswith('kor_'))
async def opis(callback:CallbackQuery, state:FSMContext):
    opi=await get_kor(callback.data.split('_')[1])

    await callback.message.edit_text(f'Название:{opi.name}\nОписание:{opi.description}\nЦена:{opi.price}',
                                     reply_markup=await nazad())
    await state.set_state(sos.CatalogState.view_korzina)
    await state.update_data(id_kor = opi.id)

@router.callback_query(F.data == 'delete')
async def delete(callback: CallbackQuery, state:FSMContext):
    data = await state.get_data()
    id_kor = data.get('id_kor')
    await del_korzina(id_kor)
    await callback.answer("Вы удалили данный товар из корзины!")





# @router.callback_query(F.data.startswith("Корзина"))
# async def view_korzina(callback:CallbackQuery):
#     tg_id = callback.from_user.id
#     await callback.message.edit_text("Товары в вашей корзине:", reply_markup=await view_kor(tg_id))



