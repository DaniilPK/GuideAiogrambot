from aiogram import types
from html import escape
from bot.language.translator import LocalizedTranslator


async def start(message: types.Message, translator: LocalizedTranslator):
    await message.answer(translator.get('start', user=escape(message.from_user.first_name)))