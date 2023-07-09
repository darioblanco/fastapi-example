.DEFAULT_GOAL := help
COMPOSE := $(shell command -v podman-compose 2> /dev/null || command -v docker-compose 2> /dev/null)
COMPOSE_FILE := container/docker-compose.yml
SHELL := /usr/bin/env bash
MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --no-builtin-variables

.PHONY: cleanup db-attach db-fixtures db-migrate db-run dev-run \
	format help init install lint \
	pre-commit server-build server-run test

cleanup: init ## cleans up all containers
	$(COMPOSE) -f $(COMPOSE_FILE) down

db-attach: init ## attach to the local database container
	$(COMPOSE) -f $(COMPOSE_FILE) exec postgres psql -U sampleapi -d sampleapi

db-fixtures: init ## load fixture data into the db
	poetry run python app/scripts/load_data.py

db-migrate: init ## apply any pending db migrations
	alembic upgrade head

db-run: init ## run the local database in a container
	$(COMPOSE) -f $(COMPOSE_FILE) up -d postgres

dev-run: init db-run ## run the local database (in a container) and the API server (without the container)
	poetry run python server.py

format: init ## format syntax code (isort and black)
	isort .
	black .
	prettier --write "**/*.{json,yaml,yml}"

help: ## list available commands
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

init: ## verify that all the required commands are already installed
	@function cmd { \
		if ! command -v "$$1" &>/dev/null ; then \
			echo "error: missing required command in PATH: $$1" >&2 ;\
			return 1 ;\
		fi \
	} ;\
	cmd python ;\
	cmd poetry ;\
	cmd prettier;\

install: init ## install project dependencies and commit hooks
	poetry install
	poetry run pre-commit install

lint: init ## lint syntax code (isort and black)
	isort -c .
	black --check .
	prettier --check "**/*.{json,yaml,yml}"

pre-commit: init ## run all pre-commit checks
	poetry run pre-commit run --all-files

server-build: init ## build the local server container
	$(COMPOSE) -f $(COMPOSE_FILE) build server

server-run: init ## run the local server in a container
	$(COMPOSE) -f $(COMPOSE_FILE) up -d server

test: init ## run tests with coverage
	pytest --cov=app --cov-report term-missing --cov-report html:htmlcov tests/
