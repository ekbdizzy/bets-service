import decimal

from pydantic import BaseModel, UUID4, FutureDatetime
from decimal import Decimal

from models import BetStatus


class CreateBetScheme(BaseModel):
    event_uuid: UUID4
    amount: decimal.Decimal


class BetScheme(CreateBetScheme):
    id: int
    status: BetStatus
    win_amount: Decimal


class EventScheme(BaseModel):
    id: UUID4
    title: str
    coefficient: Decimal
    deadline_at: FutureDatetime
    status: BetStatus
