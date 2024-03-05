from fastapi import FastAPI

from database import create_tables
from router import bet_router, event_router

app = FastAPI()
app.include_router(bet_router)
app.include_router(event_router)


@app.on_event("startup")
async def startup():
    await create_tables()


@app.get("/status", status_code=200)
async def status():
    return {"status": "ok"}
