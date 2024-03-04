from pydantic import BaseModel, FutureDatetime, UUID4, PastDatetime
from decimal import Decimal
from models import EventStatus, EventModel


class CreateEventScheme(BaseModel):
    title: str
    coefficient: Decimal
    deadline_at: FutureDatetime


class EventScheme(CreateEventScheme):
    id: UUID4
    status: EventStatus
    deadline_at: FutureDatetime | PastDatetime


class UpdateEventScheme(BaseModel):
    id: UUID4
    title: str | None = None
    status: EventStatus | None = None
    deadline_at: FutureDatetime | None = None
    coefficient: Decimal | None = None
