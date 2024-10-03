import asyncio
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
import app.keyboards as kb
import app.sost as sos

router=Router()

@router.message(CommandStart())
async def start(message:Message):
    await message.answer("Hi",  reply_markup=kb.main)

@router.message(Command("help"))
async def help(message:Message):
    await message.reply("pipi")

@router.message(F.text=="Каталог")
async def cat(message:Message):
    await message.answer("Выбери категорию товара", reply_markup=kb.catalog)

@router.callback_query(F.data=='ashot')
async def ashot(callback:CallbackQuery):
    await callback.answer('Вы выбрали категроию футболок.', show_alert=True)
    # await callback.message.answer('Вы выбрали категроию футболок.')

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

# @router.message(sos.Register.nimber, F.contact)
# async def registr_nimber(message:Message, state:FSMContext):
#     await state.update_data(nimber=message.contact.phone_number)
#     data=await state.get_data()
#     await message.answer(f'Имя:{data["name"]}\nФамилия:{data["age"]}\nВозраст:{data["age"]}\nНомер:{data["nimber"]}')
#     await state.clear()

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
    await message.answer(f'Имя:{data["name"]}\nФамилия:{data["age"]}\nВозраст:{data["age"]}\nНомер:{data["nimber"]}')
    await state.clear()
