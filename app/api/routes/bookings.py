from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.booking_repository import BookingRepository
from app.repositories.room_repository import RoomRepository
from app.schemas.booking import BookingCreate, BookingResponse
from app.services.booking_service import BookingService


router = APIRouter(
    prefix="/api/bookings",
    tags=["Bookings"],
)


def get_booking_service(
    db: Session = Depends(get_db),
) -> BookingService:

    booking_repository = BookingRepository(db)
    room_repository = RoomRepository(db)

    return BookingService(
        booking_repository=booking_repository,
        room_repository=room_repository,
    )


@router.post(
    "",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_booking(
    booking: BookingCreate,
    service: BookingService = Depends(get_booking_service),
):
    return service.create_booking(booking)


@router.get(
    "",
    response_model=list[BookingResponse],
)
def get_bookings(
    room_id: int | None = Query(default=None),
    date: date | None = Query(default=None),
    db: Session = Depends(get_db),
):
    repository = BookingRepository(db)

    return repository.get_all(
        room_id=room_id,
        booking_date=date,
    )


@router.delete(
    "/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_booking(
    booking_id: int,
    service: BookingService = Depends(get_booking_service),
):
    service.delete_booking(booking_id)