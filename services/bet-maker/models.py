from enum import Enum
from typing import Literal, get_args
from sqlalchemy import func, UUID as sa_UUID, FetchedValue, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, TIMESTAMP, ENUM
from database import Base


# BetStatus = Literal["new", "win", "lose"]


class BetStatus(Enum):
    new = "new"
    win = "win"
    lose = "lose"


class Bet(Base):

    __tablename__ = "bet"

    id: Mapped[int] = mapped_column(
        "id",
        primary_key=True,
        comment="Bet ID",
    )
    event_uuid: Mapped[sa_UUID] = mapped_column(
        "event_uuid",
        PG_UUID(as_uuid=True),
        nullable=False,
        comment="Event unique ID",
    )

    amount: Mapped[Numeric] = mapped_column(
        "amount",
        Numeric(asdecimal=True, scale=2),
        nullable=False,
        comment="Bet amount",
    )

    status: Mapped[BetStatus] = mapped_column(default=BetStatus.new)

    win_amount: Mapped[Numeric] = mapped_column(
        "win_amount",
        Numeric(asdecimal=True, scale=2),
        default="0.00",
        comment="Win amount",
    )

    created_at: Mapped[TIMESTAMP] = mapped_column(
        "created_at",
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[TIMESTAMP] = mapped_column(
        "updated_at",
        TIMESTAMP(timezone=True),
        server_onupdate=FetchedValue(),
    )

    __table_args__ = (CheckConstraint(amount > 0, name="positive_amount"), {})
