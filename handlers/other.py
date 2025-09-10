from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU

other_router = Router()

#Хендлер для ответа на сообщения которые не обрабатываются

@other_router.message()
async def other_message(message: Message):
    await message.answer(text=LEXICON_RU['other_message'])