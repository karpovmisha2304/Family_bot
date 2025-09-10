from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from lexicon.lexicon import LEXICON_RU

user_router = Router()

#Хендлер обрабатывающий команду старт
@user_router.message(CommandStart())
async def command_start(message: Message):  
    await message.answer(text=LEXICON_RU['/start'])

@user_router.message(Command(commands='help'))
async def start_info(message: Message):
    await message.answer(text=LEXICON_RU['/help'])
    
