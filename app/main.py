from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.routes.rooms import router as rooms_router
from app.api.routes.bookings import router as bookings_router
from app.db.database import get_db

app = FastAPI()

app.include_router(rooms_router)
app.include_router(bookings_router)

@app.get("/")
def root():
    return {"message": "Meeting Room Service"}


@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))
    return {"database": result.scalar()}
