from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, date

from ..database import get_db
from ..models.reservation import Reservation
from ..models.room import Room
from ..schemas.reservation import ReservationCreate
from ..auth import get_current_user

router = APIRouter(prefix="/reservations", tags=["reservations"])


@router.post("", status_code=201)
def create_reservation(
    data: ReservationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # 1. 스터디룸 존재 확인
    room = db.query(Room).filter(Room.id == data.roomId).first()
    if not room:
        raise HTTPException(status_code=404, detail={"error": "스터디룸을 찾을 수 없습니다."})

    # 2. 입력값 검증
    if not data.purpose.strip():
        raise HTTPException(status_code=400, detail={"error": "예약 목적은 필수입니다."})

    if data.startTime >= data.endTime:
        raise HTTPException(status_code=400, detail={"error": "시작 시간은 종료 시간보다 빨라야 합니다."})

    if data.startTime < "09:00" or data.endTime > "22:00":
        raise HTTPException(status_code=400, detail={"error": "예약 가능 시간은 09:00~22:00입니다."})

    # 3. 과거 날짜 체크
    reservation_date = datetime.strptime(data.date, "%Y-%m-%d").date()
    if reservation_date < date.today():
        raise HTTPException(status_code=400, detail={"error": "과거 날짜에는 예약할 수 없습니다."})

    # 4. 시간 충돌 검증
    conflicting = (
        db.query(Reservation)
        .filter(
            Reservation.room_id == data.roomId,
            Reservation.date == data.date,
            Reservation.start_time < data.endTime,
            Reservation.end_time > data.startTime,
        )
        .first()
    )
    if conflicting:
        raise HTTPException(status_code=409, detail={"error": "해당 시간대에 이미 예약이 존재합니다."})

    # 5. 예약 생성
    reservation = Reservation(
        id=f"rsv_{int(datetime.now().timestamp() * 1000)}",
        room_id=data.roomId,
        user_id=current_user.id,
        date=data.date,
        start_time=data.startTime,
        end_time=data.endTime,
        purpose=data.purpose,
    )
    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    return {
        "id": reservation.id,
        "roomId": reservation.room_id,
        "date": reservation.date,
        "startTime": reservation.start_time,
        "endTime": reservation.end_time,
        "purpose": reservation.purpose,
        "userId": current_user.id,
        "username": current_user.username,
        "createdAt": reservation.created_at.isoformat(),
    }


@router.get("/me")
def get_my_reservations(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    reservations = (
        db.query(Reservation)
        .filter(Reservation.user_id == current_user.id)
        .order_by(Reservation.date, Reservation.start_time)
        .all()
    )
    result = []
    for r in reservations:
        room = db.query(Room).filter(Room.id == r.room_id).first()
        result.append({
            "id": r.id,
            "roomId": r.room_id,
            "roomName": room.name if room else "알 수 없음",
            "date": r.date,
            "startTime": r.start_time,
            "endTime": r.end_time,
            "purpose": r.purpose,
            "userId": current_user.id,
            "username": current_user.username,
            "createdAt": r.created_at.isoformat(),
        })
    return result


@router.delete("/{reservation_id}")
def cancel_reservation(
    reservation_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail={"error": "예약을 찾을 수 없습니다."})

    if reservation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail={"error": "본인의 예약만 취소할 수 있습니다."})

    db.delete(reservation)
    db.commit()
    return {"message": "예약이 취소되었습니다."}
