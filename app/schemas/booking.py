from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class BookingCreate(BaseModel):
    room_id: int
    organizer_name: str = Field(
        min_length=1,
        max_length=100,
    )
    start_time: datetime
    end_time: datetime

    @model_validator(mode="after")
    def validate_time(self):
        now = datetime.now(self.start_time.tzinfo)

        if self.start_time < now:
            raise ValueError("start_time cannot be in the past")

        if self.end_time <= self.start_time:
            raise ValueError(
                "end_time must be greater than start_time"
            )

        return self


class BookingResponse(BaseModel):
    id: int
    room_id: int
    organizer_name: str
    start_time: datetime
    end_time: datetime

    model_config = ConfigDict(from_attributes=True)