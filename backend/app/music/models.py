"""Raw listening data. Only code inside app/music should read these tables."""

from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models import utcnow


class MusicProfile(Base):
    __tablename__ = "music_profiles"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    # Ordered favourite first: [{"name": "Frank Ocean", "genres": ["r&b", "neo soul"]}, ...]
    top_artists: Mapped[list] = mapped_column(JSON, default=list)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
