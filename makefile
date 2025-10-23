.PHONY: start

start:
	@echo "Starting docker-compose dev stack..."
	-docker compose up --build --force-recreate -d

start-dev:
	@echo "Starting docker-compose dev stack with live reload..."
	-docker compose -f docker-compose-dev.yml up --build --force-recreate -d