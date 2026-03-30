from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from ..database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    likes = Column(Integer, default=0)

    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
