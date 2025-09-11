from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
from lexicon.lexicon import LEXICON_COMMAND


#функция настройки кнопок меню
async def set_main_menu(bot: Bot):
    main_menu = [BotCommand(command=command, description=description) for command, description in LEXICON_COMMAND.items()]
    await bot.set_my_commands(commands=main_menu, scope=BotCommandScopeAllPrivateChats())

    
