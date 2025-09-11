from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import default_state, State, StatesGroup

from lexicon.lexicon import LEXICON_RU

storage = MemoryStorage()
user_router = Router()

counter = 1
user_dict: dict[int, dict[str, str | int | bool]] = {}


class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    fill_name = State()        # имя товара
    fill_price = State()         # цена товара

#Хендлер обрабатывающий команду старт
@user_router.message(CommandStart())
async def command_start(message: Message):  
    await message.answer(text=LEXICON_RU['/start'])

@user_router.message(Command(commands='help'))
async def start_info(message: Message):
    await message.answer(text=LEXICON_RU['/help'])
    
@user_router.message(Command(commands='add'), StateFilter(default_state))
async def add_purchases(message: Message, state: FSMContext):
    await message.answer(text='введите наименование продукта')
    await state.set_state(FSMFillForm.fill_name)
    
@user_router.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def name_product(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text='Имя записано\nТеперь введите стоимость товара')
    await state.set_state(FSMFillForm.fill_price)

@user_router.message(StateFilter(FSMFillForm.fill_price), lambda x: x.text.isdigit())
async def price_purchases(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    user_dict = await state.get_data()
    print(user_dict)
    print(user_dict['name'], user_dict['price'])
    await state.clear()
    await message.answer(text='Цена записана\n\nДля продолжения выберите команду в Меню')
    
@user_router.message(Command(commands='view'), StateFilter(default_state))
async def view_purchases(message: Message):
    print(user_dict)
    if user_dict:
        await message.answer(user_dict['name'], user_dict['price'])
    else:
        await message.answer(text='Покупки еще не внесены\nВыберите дальнейшие действия в Меню')