from enum import Enum
from sqlalchemy import func, UUID as sa_UUID, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, TIMESTAMP
from database import Base


class EventStatus(Enum):
    new = "new"
    win = "win"
    lose = "lose"


class EventModel(Base):
    __tablename__ = "event"

    id: Mapped[sa_UUID] = mapped_column(
        "id",
        PG_UUID(as_uuid=True),
        primary_key=True,
        comment="Event ID",
    )

    coefficient: Mapped[Numeric] = mapped_column(
        "coefficient",
        Numeric(asdecimal=True, scale=2),
        nullable=False,
        comment="Coefficient",
    )

    status: Mapped[EventStatus] = mapped_column(default=EventStatus.new)

    created_at: Mapped[TIMESTAMP] = mapped_column(
        "created_at",
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )

    deadline_at: Mapped[TIMESTAMP] = mapped_column(
        "deadline_at", TIMESTAMP(timezone=True), comment="Deadline for getting bets."
    )

    __table_args__ = (
        CheckConstraint(coefficient > 0, name="positive_amount"),
        CheckConstraint(deadline_at > created_at, name="correct_deadline"),
        {},
    )
