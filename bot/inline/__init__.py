from aiogram import Router

from bot.inline.message import inline_echo


def register_inline(router: Router):
    router.inline_query.register(inline_echo)
