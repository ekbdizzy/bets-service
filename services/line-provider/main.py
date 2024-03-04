from fastapi import FastAPI
from database import create_tables
from router import event_router

app = FastAPI()
app.include_router(event_router)


@app.on_event("startup")
async def startup():
    await create_tables()
