from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from tzlocal import get_localzone
import zoneinfo

from settings import redis
from schemes import CreateEventScheme, EventScheme, UpdateEventScheme
from database import db_session
from models import EventModel
from datetime import datetime


async def redis_set_event(event: EventScheme, publish: bool = False) -> None:
    """Set key = event ID and value with event data and expired period equal to deadline of event.
    :param event: event,
    :param publish: publish message to channel 'events' if publish = True."""
    async with redis.client() as conn:
        now = datetime.now(tz=zoneinfo.ZoneInfo(get_localzone().key))
        expired = (event.deadline_at - now).total_seconds()
        await conn.set(
            f"event:{str(event.id)}",
            event.json(
                exclude={"id"},
            ),
            ex=int(expired),
        )
        if publish:
            await redis.publish(channel="events", message=event.json())


class EventHandler:

    @staticmethod
    async def create(event: CreateEventScheme) -> EventScheme:
        """Method to create new event."""
        async with db_session() as session:
            event = EventModel(**event.model_dump())
            session.add(event)
            await session.commit()
            await session.refresh(event)
            result = EventScheme.model_validate(event.__dict__)

            await redis_set_event(result)
            return result

    @staticmethod
    async def get_list() -> list[EventScheme]:
        """Method to get list of events."""
        async with db_session() as session:
            query = select(EventModel)
            events = await session.execute(query)
            events = events.scalars().all()
            response = [EventScheme.model_validate(event.__dict__) for event in events]
            return response

    @staticmethod
    async def update(event: UpdateEventScheme) -> EventScheme:
        """Method to update event."""
        async with db_session() as session:
            try:
                existing_event = await session.execute(
                    select(EventModel).filter_by(id=event.id)
                )
                event_model = existing_event.scalars().first()
                if event_model:
                    for key, value in event.dict(exclude_none=True).items():
                        setattr(event_model, key, value)
                else:
                    raise NoResultFound

                await session.commit()
                await session.refresh(event_model)

                result = EventScheme.model_validate(event_model.__dict__)
                await redis_set_event(result, publish=True)
                return result

            except NoResultFound:
                raise HTTPException(status_code=404, detail="Event not found")
