## Bets Service
Service for managing bets and events on FastAPI, SQLAlchemy, Postgres, Redis.

Contains 2 microservices:
* `bet-maker` - API for managing bets. 
* `line-provider` - API for managing events.

Bet updates are based on Redis messages.<br>
Actual events for bets are based on Redis `event:*` keys with `expire=deadline`. 
<br> After the event status is updated, it will make changes to the bet status and win amount.

---

## How to start:
1. Create `.env` files inside services.
```shell
make create_env
```
2. Run project:
```shell
make start
```

Once started, both services, databases, redis and redis_gui will start working.

`bet-maker`: http://localhost:8000 <br>
`line-provider`: http://localhost:8001 <br>
`redis_gui`: http://localhost:9000
