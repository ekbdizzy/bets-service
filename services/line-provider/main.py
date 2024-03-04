from fastapi import FastAPI
from database import create_tables

app = FastAPI()


@app.on_event("startup")
async def startup():
    await create_tables()
