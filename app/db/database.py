from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.db.models import Base, Room

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{settings.postgres_user}:"
    f"{settings.postgres_password}@"
    f"{settings.postgres_host}:"
    f"{settings.postgres_port}/"
    f"{settings.postgres_db}"
)


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def init_db():
    Base.metadata.create_all(bind=engine)


def seed_rooms():
    db = SessionLocal()

    try:
        rooms = db.query(Room).count()

        if rooms == 0:
            db.add_all(
                [
                    Room(
                        name="Meeting Room 1",
                        capacity=6,
                    ),
                    Room(
                        name="Meeting Room 2",
                        capacity=10,
                    ),
                    Room(
                        name="Conference Room",
                        capacity=20,
                    ),
                ]
            )

            db.commit()
    finally:
        db.close()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
