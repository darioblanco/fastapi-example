.DEFAULT_GOAL := help
COMPOSE := $(shell command -v podman-compose 2> /dev/null || command -v docker-compose 2> /dev/null)
COMPOSE_FILE := container/docker-compose.yml
SHELL := /usr/bin/env bash
MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --no-builtin-variables

.PHONY: app-build app-run \
	db-attach db-destroy db-run \
	db-test-attach db-test-destroy db-test-run \
	format help init install lint \
	load-fixtures migrate pre-commit run test validate

app-build: init ## build the local app container
	$(COMPOSE) -f $(COMPOSE_FILE) build app

app-run: init ## run the local app in a container
	$(COMPOSE) -f $(COMPOSE_FILE) up -d app

clean: init ## cleans up all containers and other temporary files
	$(COMPOSE) -f $(COMPOSE_FILE) down

db-attach: init ## attach to the local database container
	$(COMPOSE) -f $(COMPOSE_FILE) exec db psql -U sampleapi -d sampleapi

db-destroy: init ## run the local database in a container
	$(COMPOSE) -f $(COMPOSE_FILE) down db

db-run: init ## run the local database in a container
	$(COMPOSE) -f $(COMPOSE_FILE) up -d db

db-test-attach: init ## attach to the local database container for testing
	$(COMPOSE) -f $(COMPOSE_FILE) exec db-test psql -U sampleapi -d test_sampleapi

db-test-destroy: init ## destroy to the local database container for testing
	$(COMPOSE) -f $(COMPOSE_FILE) down db-test

db-test-run: init ## run the local database in a container for testing
	$(COMPOSE) -f $(COMPOSE_FILE) up -d db-test

docs: init ## generate sphinx documentation for the code
	poetry run sphinx-build -b html docs/ docs/_build

format: init ## format syntax code (isort and black)
	poetry run isort .
	poetry run black .
	prettier --write "**/*.{json,yaml,yml}"

help: ## list available commands
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

init: ## verify that all the required commands are already installed
	@if [ -z "$$CI" ]; then \
		function cmd { \
			if ! command -v "$$1" &>/dev/null ; then \
				echo "error: missing required command in PATH: $$1" >&2 ;\
				return 1 ;\
			fi \
		} ;\
		cmd kubeconform ;\
		cmd python ;\
		cmd poetry ;\
		cmd prettier;\
		cmd yq ;\
	fi

install: init ## install project dependencies and commit hooks
	poetry install
	@if [ -z "$$CI" ]; then \
		poetry run pre-commit install ; \
	fi

lint: init ## lint syntax code (isort and black)
	poetry run isort -c .
	poetry run black --check .

load-fixtures: init ## load fixture data into the db
	poetry run python app/scripts/load_data.py

migrate: init ## apply any pending db migrations
	poetry run alembic upgrade head

pre-commit: init ## run all pre-commit checks
	poetry run pre-commit run --all-files

run: init ## run the local database (in a container) and the API server (without the container)
	@$(MAKE) db-run --quiet > /dev/null 2>&1
	poetry run python server.py

ifdef CI

# run tests with coverage in a CI environment
test:
	poetry run pytest --cov=app --cov-report term-missing --cov-report html:htmlcov tests/
else

test: init ## run tests with coverage in the local environment, creating and destroying the test db
	@$(MAKE) db-test-run --quiet > /dev/null 2>&1
	poetry run pytest --cov=app --cov-report term-missing --cov-report html:htmlcov tests/
	@$(MAKE) db-test-destroy --quiet > /dev/null 2>&1

endif

validate: init ## validate the kustomize resources using kubeconform
	./scripts/validate.sh
