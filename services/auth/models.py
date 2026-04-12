from datetime import datetime, timezone

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class TimeStampedModel(SQLModel):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class User(TimeStampedModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)

    email: EmailStr = Field(max_length=200, unique=True)
    hashed_password: str = Field()
