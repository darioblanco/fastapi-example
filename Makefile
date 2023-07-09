.DEFAULT_GOAL := help
COMPOSE := $(shell command -v podman-compose 2> /dev/null || command -v docker-compose 2> /dev/null)
COMPOSE_FILE := container/docker-compose.yml
SHELL := /usr/bin/env bash
MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --no-builtin-variables

.PHONY: cleanup db-attach db-fixtures db-migrate db-run dev-run \
	format help install lint \
	server-build server-run test

cleanup: ## cleans up all containers
	$(COMPOSE) -f $(COMPOSE_FILE) down

db-attach: ## attach to the local database container
	$(COMPOSE) -f $(COMPOSE_FILE) exec postgres psql -U sampleapi -d sampleapi

db-fixtures: ## load fixture data into the db
	poetry run python app/scripts/load_data.py

db-migrate: ## apply any pending db migrations
	alembic upgrade head

db-run: ## run the local database in a container
	$(COMPOSE) -f $(COMPOSE_FILE) up -d postgres

dev-run: db-run ## run the local database (in a container) and the API server (without the container)
	poetry run python server.py

format: ## format syntax code (isort and black)
	isort .
	black .

help: ## list available commands
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## install project dependencies
	poetry install

lint: ## lint syntax code (isort and black)
	isort -c .
	black --check .

server-build: ## build the local server container
	$(COMPOSE) -f $(COMPOSE_FILE) build server

server-run: ## run the local server in a container
	$(COMPOSE) -f $(COMPOSE_FILE) up -d server

test: ## run tests with coverage
	pytest --cov=app --cov-report term-missing --cov-report html:htmlcov tests/
