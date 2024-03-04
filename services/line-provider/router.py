from fastapi import APIRouter
from handlers import EventHandler

event_router = APIRouter(
    prefix="/events",
    tags=["events"],
)

event_router.add_api_route(
    "",
    endpoint=EventHandler.create,
    methods=["POST"],
    status_code=201,
    summary="Create new event",
)

event_router.add_api_route(
    "",
    endpoint=EventHandler.get_list,
    methods=["GET"],
    status_code=200,
    summary="Get events",
)

event_router.add_api_route(
    path="/{id}",
    endpoint=EventHandler.update,
    methods=["PATCH"],
    status_code=200,
    summary="Update event",
)
