from aiogram import Router, F
from aiogram.filters import CommandStart

from bot.handlers.start import start


def router_register(router: Router):
    router.message.filter(F.chat.type == 'private')

    router.message.register(start,CommandStart())