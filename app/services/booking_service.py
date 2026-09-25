from fastapi import HTTPException, status

from app.db.models import Booking
from app.repositories.booking_repository import BookingRepository
from app.repositories.room_repository import RoomRepository
from app.schemas.booking import BookingCreate


class BookingService:
    def __init__(
        self,
        booking_repository: BookingRepository,
        room_repository: RoomRepository,
    ):
        self.booking_repository = booking_repository
        self.room_repository = room_repository

    def create_booking(
        self,
        booking_data: BookingCreate,
    ) -> Booking:

        room = self.room_repository.get_by_id(
            booking_data.room_id
        )

        if room is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found",
            )

        overlapping_booking = (
            self.booking_repository.get_overlapping_booking(
                room_id=booking_data.room_id,
                start_time=booking_data.start_time,
                end_time=booking_data.end_time,
            )
        )

        if overlapping_booking is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Room is already booked for this time",
            )

        booking = Booking(
            room_id=booking_data.room_id,
            organizer_name=booking_data.organizer_name,
            start_time=booking_data.start_time,
            end_time=booking_data.end_time,
        )

        return self.booking_repository.create(booking)

    def delete_booking(self, booking_id: int) -> None:
        booking = self.booking_repository.get_by_id(
            booking_id
        )

        if booking is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found",
            )

        self.booking_repository.delete(booking)