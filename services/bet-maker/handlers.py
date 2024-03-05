from sqlalchemy import select, update
from database import db_session
from settings import redis
from schemes import CreateBetScheme, BetScheme, EventScheme
from models import Bet
import json


class BetHandler:
    @staticmethod
    async def create(bet: CreateBetScheme) -> BetScheme:
        async with db_session() as session:
            new_bet = Bet(**bet.dict())
            session.add(new_bet)
            await session.commit()
            await session.refresh(new_bet)
            result = BetScheme.model_validate(new_bet.__dict__)
            return result

    @staticmethod
    async def get_list() -> list[BetScheme]:
        async with db_session() as session:
            query = select(Bet)
            res = await session.execute(query)
            bets = res.scalars().all()
            result = [BetScheme.model_validate(bet.__dict__) for bet in bets]
            return result

    @staticmethod
    async def update_bets_status(event_dict: EventScheme):
        event = EventScheme.model_validate(event_dict)
        async with db_session() as session:
            query = update(Bet).filter_by(event_uuid=event.id)
            match event.status.value:
                case "win":
                    query = query.values(
                        status="win",
                        win_amount=Bet.amount * event.coefficient,
                    )
                case "lose":
                    query = query.values(status="lose")
            await session.execute(query)
            await session.commit()


class EventHandler:
    @staticmethod
    async def get_list() -> list[EventScheme]:
        """Get actual events list from redis."""
        async with redis.client() as conn:
            keys = await conn.keys("event:*")
            events = []
            for key in keys:
                event = json.loads(await redis.get(key))
                event["id"] = key.split(":")[1]
                events.append(event)
            result = [EventScheme.model_validate(event) for event in events]
            return result
