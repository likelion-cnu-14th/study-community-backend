from sqlalchemy import Column, String, Integer, Text, JSON

from ..database import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(String, primary_key=True)
    name = Column(String(100), nullable=False)
    location = Column(String(200), nullable=False)
    capacity = Column(Integer, nullable=False)
    description = Column(Text, default="")
    amenities = Column(JSON, default=list)
