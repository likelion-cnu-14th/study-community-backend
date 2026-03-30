from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from ..database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(String, primary_key=True)
    content = Column(Text, nullable=False)
    author = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    post_id = Column(String, ForeignKey("posts.id"), nullable=False)

    post = relationship("Post", back_populates="comments")
