from pydantic import BaseModel, ConfigDict


class RoomResponse(BaseModel):
    id: int
    name: str
    capacity: int

    model_config = ConfigDict(from_attributes=True)