from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.room import Room
from ..models.reservation import Reservation
from ..models.user import User

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("")
def get_rooms(db: Session = Depends(get_db)):
    rooms = db.query(Room).all()
    return [
        {
            "id": r.id,
            "name": r.name,
            "location": r.location,
            "capacity": r.capacity,
            "description": r.description,
            "amenities": r.amenities or [],
        }
        for r in rooms
    ]


@router.get("/{room_id}")
def get_room(room_id: str, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail={"error": "스터디룸을 찾을 수 없습니다."})
    return {
        "id": room.id,
        "name": room.name,
        "location": room.location,
        "capacity": room.capacity,
        "description": room.description,
        "amenities": room.amenities or [],
    }


@router.get("/{room_id}/reservations")
def get_room_reservations(
    room_id: str,
    date: str = Query(..., description="조회할 날짜 (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail={"error": "스터디룸을 찾을 수 없습니다."})

    reservations = (
        db.query(Reservation)
        .filter(Reservation.room_id == room_id, Reservation.date == date)
        .order_by(Reservation.start_time)
        .all()
    )

    result = []
    for r in reservations:
        user = db.query(User).filter(User.id == r.user_id).first()
        result.append({
            "id": r.id,
            "roomId": r.room_id,
            "date": r.date,
            "startTime": r.start_time,
            "endTime": r.end_time,
            "purpose": r.purpose,
            "userId": r.user_id,
            "username": user.username if user else "알 수 없음",
            "createdAt": r.created_at.isoformat(),
        })
    return result
