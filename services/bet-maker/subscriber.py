import asyncio
import json
from contextlib import suppress

import async_timeout
import aioredis.client
from handlers import BetHandler


async def listen_events(redis_client: aioredis.client):
    redis_pubsub = redis_client.pubsub()
    await redis_pubsub.subscribe("events")
    while True:
        with suppress(asyncio.TimeoutError):
            async with async_timeout.timeout(1):
                message = await redis_pubsub.get_message(ignore_subscribe_messages=True)
                if message is not None:
                    event = json.loads(message["data"])
                    await BetHandler.update_bets_status(event)
            await asyncio.sleep(1)
