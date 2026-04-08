from pydantic import BaseModel


class RoomResponse(BaseModel):
    id: str
    name: str
    location: str
    capacity: int
    description: str
    amenities: list[str]
