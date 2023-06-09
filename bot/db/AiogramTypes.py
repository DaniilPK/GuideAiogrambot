from sqlalchemy import Integer, VARCHAR, Select, String, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from bot.db import BaseModel


class AiogramTypes(BaseModel):
    __tablename__ = 'aiogramtypes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    message_text: Mapped[str] = mapped_column(String, nullable=False)
    message_url: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)


async def getTypes(session: AsyncSession,query,offset = 50):
    return await session.execute(Select(AiogramTypes).filter(func.lower(AiogramTypes.title).like(f'%{query}%')).limit(offset))

