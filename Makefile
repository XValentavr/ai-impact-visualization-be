remove-volumes:
	docker-compose down --volumes

start:
	docker compose up

build:
	docker compose build

stop:
	docker compose down

lint:
	pre-commit run --all-files