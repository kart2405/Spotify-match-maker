"""Dating-side tables. Music data lives in app/music/models.py."""

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def utcnow():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    spotify_id: Mapped[str | None] = mapped_column(String(100), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int | None] = mapped_column(Integer)
    city: Mapped[str] = mapped_column(String(100), default="")
    bio: Mapped[str] = mapped_column(Text, default="")
    gender: Mapped[str] = mapped_column(String(20), default="")  # "man", "woman", "nonbinary"
    interested_in: Mapped[str] = mapped_column(String(20), default="everyone")  # "men", "women", "everyone"
    # Whether shared artists may be shown to people you're browsing.
    share_artists: Mapped[bool] = mapped_column(Boolean, default=True)
    is_fake: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Like(Base):
    """A like (liked=True) or a pass (liked=False) from one user on another."""

    __tablename__ = "likes"
    __table_args__ = (UniqueConstraint("from_user_id", "to_user_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    from_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    to_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    liked: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
