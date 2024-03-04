from typing import Mapping, Annotated

from fastapi import FastAPI, Depends
from sqlalchemy import select

from schemas.bet_schemas import BetCreate
from database import db_session, create_tables

from models import Bet, BetStatus

app = FastAPI()


@app.on_event("startup")
async def startup():
    await create_tables()


@app.get("/status", status_code=200)
async def status():
    return {"status": "ok"}


@app.post("/bet", status_code=201)
async def create_bet(bet: Annotated[BetCreate, Depends()]) -> Mapping:
    async with db_session() as session:
        # async with db_conn() as session:
        new_bet = Bet(
            event_uuid=bet.event_uuid, amount=bet.amount, status=BetStatus.new
        )
        res = session.add(new_bet)
        await session.flush()
        await session.commit()
        return {"res": res}


@app.get("/bet", status_code=200)
async def get_bets():
    async with db_session() as session:
        query = select(Bet)
        res = await session.execute(query)
        bets = res.scalars().all()
        # sTask.model_validate(task_model) for task_model in task_models 32:
        return bets
