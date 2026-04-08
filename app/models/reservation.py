from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from datetime import datetime, timezone

from ..database import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(String, primary_key=True)
    room_id = Column(String, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(String(10), nullable=False)       # "2026-04-10"
    start_time = Column(String(5), nullable=False)   # "09:00"
    end_time = Column(String(5), nullable=False)     # "11:00"
    purpose = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
