from fastapi import APIRouter

from handlers import BetHandler, EventHandler

bet_router = APIRouter(
    prefix="/bets",
    tags=["Bets"],
)

bet_router.add_api_route(
    "",
    BetHandler.create,
    methods=["POST"],
    status_code=201,
    summary="Create new bet",
)

bet_router.add_api_route(
    "",
    BetHandler.get_list,
    methods=["GET"],
    status_code=200,
    summary="Get bets list",
)

event_router = APIRouter(
    prefix="/events",
    tags=["Events"],
)

event_router.add_api_route(
    "",
    EventHandler.get_list,
    methods=["GET"],
    status_code=200,
    summary="Get events list",
)
