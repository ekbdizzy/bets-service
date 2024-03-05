create_env:
	cp env.sample services/bet-maker/env & cp env.sample services/line-provider/.env

start:
	sudo docker compose up --build