import decimal

from pydantic import BaseModel, UUID4, Field, validator


class BetCreate(BaseModel):
    event_uuid: UUID4
    amount: decimal.Decimal
