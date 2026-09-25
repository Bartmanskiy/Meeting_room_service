from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.room_repository import RoomRepository
from app.schemas.room import RoomResponse


router = APIRouter(
    prefix="/api/rooms",
    tags=["Rooms"],
)


@router.get("", response_model=list[RoomResponse])
def get_rooms(db: Session = Depends(get_db)):
    repository = RoomRepository(db)

    return repository.get_all()