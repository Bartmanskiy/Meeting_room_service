from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Room


class RoomRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Room]:
        statement = select(Room).order_by(Room.id)

        return list(self.db.scalars(statement).all())

    def get_by_id(self, room_id: int) -> Room | None:
        statement = select(Room).where(Room.id == room_id)

        return self.db.scalar(statement)