from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from schemes import CreateEventScheme, EventScheme, UpdateEventScheme
from database import db_session
from models import EventModel


class EventHandler:

    @staticmethod
    async def create(event: CreateEventScheme):
        async with db_session() as session:
            event = EventModel(**event.model_dump())
            session.add(event)
            await session.commit()
            await session.refresh(event)
            return event

    @staticmethod
    async def get_list() -> list[EventScheme]:
        async with db_session() as session:
            query = select(EventModel)
            events = await session.execute(query)
            events = events.scalars().all()
            response = [EventScheme.model_validate(event.__dict__) for event in events]
            return response

    @staticmethod
    async def update(event: UpdateEventScheme) -> EventScheme:
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
                return EventScheme.model_validate(event_model.__dict__)

            except NoResultFound:
                raise HTTPException(status_code=404, detail="Event not found")
