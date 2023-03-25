from aiogram import types
from aiogram.utils.markdown import hlink
from redis.asyncio.client import Redis

from bot.db import getTypes, getMethods
from bot.db.AiogramTypes import AiogramTypes


async def inline_echo(inline_query: types.InlineQuery, session, redis: Redis):
    query = inline_query.query.lower()
    results = []
    value = await redis.get(str(inline_query.from_user.id))

    if query == 'list':
        await redis.delete(str(inline_query.from_user.id))
        return await inline_query.answer(results=[
            types.InlineQueryResultArticle(id=0, title='Вам нужно выбрать один из разделов. Types или Methods',
                                           input_message_content=types.InputTextMessageContent(message_text='.'),
                                           description='@aiogram_support_bot Types или Methods',
                                           )], cache_time=0, is_personal=True)
    elif query == 'types':
        await redis.set(name=str(inline_query.from_user.id), value='types')
        return await inline_query.answer(results=[
            types.InlineQueryResultArticle(id=0, title='Выбран раздел types. Введите запрос для поиска типа',
                                           input_message_content=types.InputTextMessageContent(message_text='.'),
                                           )], cache_time=0, is_personal=True)
    elif query == 'methods':
        await redis.set(name=str(inline_query.from_user.id), value='methods')
        return await inline_query.answer(results=[
            types.InlineQueryResultArticle(id=0, title='Выбран раздел Methods. Введите запрос для поиска метода',
                                           input_message_content=types.InputTextMessageContent(message_text='.'),
                                           )], cache_time=0, is_personal=True)
    elif value is not None:
        results.append(types.InlineQueryResultArticle(id=0, title='Что бы посмотреть разделы напишите "list"',
                                                      input_message_content=types.InputTextMessageContent(
                                                          message_text='.'),
                                                      description='@aiogram_support_bot list'))
        if value == b'methods':
            res = await getMethods(session, query, 49)
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
        elif value == b'types':
            res = await getTypes(session, query, 49)
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
        return await inline_query.answer(results=results, cache_time=0, is_personal=True)
    else:
        results.append(types.InlineQueryResultArticle(
            id=0,
            title='Вам нужно выбрать один из разделов. Types или Methods',
            input_message_content=types.InputTextMessageContent(
                message_text='.',
            ),
            description='@aiogram_support_bot Types или Methods',
        ))
        return await inline_query.answer(results=results, cache_time=0, is_personal=True)
