from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Booking


class BookingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_overlapping_booking(
        self,
        room_id: int,
        start_time: datetime,
        end_time: datetime,
    ) -> Booking | None:

        statement = select(Booking).where(
            Booking.room_id == room_id,
            Booking.start_time < end_time,
            Booking.end_time > start_time,
        )

        return self.db.scalar(statement)

    def create(self, booking: Booking) -> Booking:
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)

        return booking

    def get_all(
        self,
        room_id: int | None = None,
        booking_date: date | None = None,
    ) -> list[Booking]:

        statement = select(Booking)

        if room_id is not None:
            statement = statement.where(
                Booking.room_id == room_id
            )

        if booking_date is not None:
            start_of_day = datetime.combine(
                booking_date,
                datetime.min.time(),
            )

            end_of_day = datetime.combine(
                booking_date,
                datetime.max.time(),
            )

            statement = statement.where(
                Booking.start_time >= start_of_day,
                Booking.start_time <= end_of_day,
            )

        statement = statement.order_by(Booking.start_time)

        return list(self.db.scalars(statement).all())

    def get_by_id(self, booking_id: int) -> Booking | None:
        statement = select(Booking).where(
            Booking.id == booking_id
        )

        return self.db.scalar(statement)

    def delete(self, booking: Booking) -> None:
        self.db.delete(booking)
        self.db.commit()