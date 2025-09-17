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
    user_dict[message.from_user.id] = await state.get_data()
    print(user_dict[message.from_user.id])
    string = ' '.join(v for k, v in user_dict[message.from_user.id].items()) + '\n'
    
    with open ('C:/проекты_пайтон/Family_bot/purchases.txt', 'a', encoding='utf-8') as file:
        file.write(string)
    await state.clear()
    await message.answer(text='Цена записана\n\nДля продолжения выберите команду в Меню')
    
@user_router.message(Command(commands='view'))
async def view_purchases(message: Message):
    with open ('C:/проекты_пайтон/Family_bot/purchases.txt', 'r', encoding='utf-8') as file:
        rd = file.read()
        print(rd, len(rd))
        if len(rd) > 0:
            await message.answer(text=f'{rd}')
        else:
            await message.answer(text='Покупки еще не внесены\nВыберите дальнейшие действия в Меню')
            
@user_router.message(Command(commands='del'))
async def del_purchases(message: Message):
    with open ('C:/проекты_пайтон/Family_bot/purchases.txt', 'w', encoding='utf-8') as file:
        await message.answer(text=LEXICON_RU['/del'])