from pydantic import EmailStr
from sqlmodel import select

from auth.db import get_async_session
from auth.models import User
from auth.password import hash_password


async def get_user_by_id(id: int) -> User | None:
    async with get_async_session() as session:
        result = await session.exec(
            select(User).where(User.id == id)
        )
        user = result.first()
        return user


async def get_user_by_email(email: EmailStr) -> User | None:
    async with get_async_session() as session:
        result = await session.exec(
            select(User).where(User.email == email)
        )
        user = result.first()
        return user


async def user_create(email: EmailStr, password: str) -> User:
    async with get_async_session() as session:
        hashed_password = hash_password(password)
        user = User(email=email, hashed_password=hashed_password)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
