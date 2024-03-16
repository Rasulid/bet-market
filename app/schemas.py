from pydantic import BaseModel, condecimal

from models import EventStatus, BetStatus


class BetSchema(BaseModel):
    id: int
    status: BetStatus

    class Config:
        orm_mode = True


class EventSchema(BaseModel):
    status: EventStatus


class BetCreate(BaseModel):
    event_id: int
    amount: condecimal(gt=0, decimal_places=2)

    class Config:
        orm_mode = True


class UpdateEvent(BaseModel):
    status: EventStatus


class CreateEvent(BaseModel):
    status: EventStatus

    class Config:
        orm_mode = True


class EventList(BaseModel):
    id: int
    status: EventStatus

    class Config:
        orm_mode = True
