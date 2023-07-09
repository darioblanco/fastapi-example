.DEFAULT_GOAL := help
COMPOSE := $(shell command -v podman-compose 2> /dev/null || command -v docker-compose 2> /dev/null)
COMPOSE_FILE := container/docker-compose.yml
SHELL := /usr/bin/env bash
MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --no-builtin-variables

.PHONY: clean db-load db-migrate dev-run \
	postgres-attach postgres-destroy postgres-run \
	postgres-test-attach postgres-test-destroy postgres-test-run \
	format help init install lint \
	pre-commit server-build server-run test

clean: init ## cleans up all containers and other temporary files
	$(COMPOSE) -f $(COMPOSE_FILE) down

db-load: init ## load fixture data into the db
	poetry run python app/scripts/load_data.py

db-migrate: init ## apply any pending db migrations
	alembic upgrade head

dev-run: init postgres-run ## run the local database (in a container) and the API server (without the container)
	poetry run python server.py

postgres-attach: init ## attach to the local database container
	$(COMPOSE) -f $(COMPOSE_FILE) exec postgres psql -U sampleapi -d sampleapi

postgres-destroy: init ## run the local database in a container
	$(COMPOSE) -f $(COMPOSE_FILE) down postgres

postgres-run: init ## run the local database in a container
	$(COMPOSE) -f $(COMPOSE_FILE) up -d postgres

postgres-test-attach: init ## attach to the local database container for testing
	$(COMPOSE) -f $(COMPOSE_FILE) exec postgres-test psql -U sampleapi -d test_sampleapi

postgres-test-destroy: init ## destroy to the local database container for testing
	$(COMPOSE) -f $(COMPOSE_FILE) down postgres-test

postgres-test-run: init ## run the local database in a container for testing
	$(COMPOSE) -f $(COMPOSE_FILE) up -d postgres-test

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
	@if [ -z "$$CI" ]; then \
		poetry run pre-commit install ; \
	fi

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

ifdef CI

test: ## run tests with coverage in a CI environment
	pytest --cov=app --cov-report term-missing --cov-report html:htmlcov tests/

else

test: init ## run tests with coverage in the local environment, creating and destroying the test db
	@$(MAKE) postgres-test-run --quiet > /dev/null 2>&1
	pytest --cov=app --cov-report term-missing --cov-report html:htmlcov tests/
	@$(MAKE) postgres-test-destroy --quiet > /dev/null 2>&1

endif
