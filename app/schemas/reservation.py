from pydantic import BaseModel


class ReservationCreate(BaseModel):
    roomId: str
    date: str          # "YYYY-MM-DD"
    startTime: str     # "HH:MM"
    endTime: str       # "HH:MM"
    purpose: str


class ReservationResponse(BaseModel):
    id: str
    roomId: str
    date: str
    startTime: str
    endTime: str
    purpose: str
    userId: str
    username: str
    createdAt: str
    roomName: str | None = None
