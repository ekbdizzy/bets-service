import asyncio

from fastapi import FastAPI

from database import create_tables
from settings import redis
from router import bet_router, event_router
from subscriber import listen_events

app = FastAPI()
app.include_router(bet_router)
app.include_router(event_router)


@app.on_event("startup")
async def startup():
    await create_tables()


asyncio.create_task(listen_events(redis))
