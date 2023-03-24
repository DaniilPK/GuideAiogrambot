from aiogram import types
from aiogram.utils.markdown import hlink

from bot.db import get
from bot.db.AiogramTypes import AiogramTypes


async def inline_echo(inline_query: types.InlineQuery, session):
    query = inline_query.query.lower()
    res = await get(session, query, 50)

    results = []

    for item in res.all():
        item: AiogramTypes = item[0]
        if query in item.title.lower():
            results.append(types.InlineQueryResultArticle(
                id=item.id,
                title=item.title,
                input_message_content=types.InputTextMessageContent(
                    message_text=hlink(item.message_text, item.message_url)),
                description=item.description
            ))
    await inline_query.answer(results=results, cache_time=60)

