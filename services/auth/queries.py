from typing import Any

from pydantic import EmailStr
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from auth.db import get_async_session
from auth.exceptions import EmailAlreadyUsedError
from auth.models import User
from auth.password import hash_password
from common.models import model_update


async def get_user_by_id(
    session: AsyncSession | None = None,
    *,
    id: int,
) -> User | None:
    if not session:
        session = get_async_session()
    async with session as s:
        result = await s.exec(select(User).where(User.id == id))
        user = result.first()
        return user


async def get_user_by_email(
    session: AsyncSession | None = None,
    *,
    email: EmailStr,
) -> User | None:
    if not session:
        session = get_async_session()

    async with session as s:
        result = await s.exec(select(User).where(User.email == email))
        user = result.first()
        return user


async def user_create(
    session: AsyncSession | None = None,
    *,
    email: EmailStr,
    password: str,
) -> User:
    """
    raises `EmailAlreadyUsedError`
    """
    other_user = await get_user_by_email(session=session, email=email)
    if other_user:
        raise EmailAlreadyUsedError(
            f'Could not create user with email {email}. Already in use'
        )

    if not session:
        session = get_async_session()

    async with session as s:
        hashed_password = hash_password(password)
        user = User(email=email, hashed_password=hashed_password)
        s.add(user)
        await s.commit()
        await s.refresh(user)
        return user


async def user_update(
    *,
    user: User,
    session: AsyncSession | None = None,
    **fields: Any,
) -> User:
    if not session:
        session = get_async_session()

    user, updates = model_update(model=user, **fields)
    if not updates:
        return user

    async with session as s:
        s.add(user)
        await s.commit()
        await s.refresh(user)
        return user
