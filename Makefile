.DEFAULT_GOAL := help 

.PHONY: help
help:  ## Show this help.
	@grep -E '^\S+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

.PHONY: build
build: ## Install the app packages
	docker build -t server .

.PHONY: up
up: ## Start the stack
	docker compose up --build

.PHONY: down
down: ## Stop and remove all the Docker services, volumes and networks
	docker compose down -v --remove-orphans

.PHONY: install
install: ## Install the app packages
	rm -rf poetry.lock
	poetry install --no-root

.PHONY: update
update: ## Updates the app packages
	poetry update

.PHONY: add-package
add-package: ## Installs a new package in the app. ex: make add-package package=XXX
	poetry add $(package)
	poetry install --no-root

.PHONY: check-typing
check-typing:  ## Run a static analyzer over the code to find issues
	poetry run mypy .

.PHONY: check-lint
check-lint: ## Checks the code style
	poetry run ruff check

.PHONY: lint
lint: ## Lints the code format
	poetry run ruff check --fix

.PHONY: check-format
check-format:  ## Check format python code
	poetry run ruff format --check

.PHONY: format
format:  ## Format python code
	poetry run ruff format

.PHONY: test-unit
test-unit: ## Run unit tests
	poetry run pytest -n auto tests/unit -ra

.PHONY: test-integration
test-integration: ## Run integration tests
	docker compose run --build --rm --entrypoint /code/scripts/test-entrypoint.sh server poetry run pytest tests/integration -ra

.PHONY: test-acceptance
test-acceptance: ## Run acceptance tests
	docker compose run --build --rm --entrypoint /code/scripts/test-entrypoint.sh server poetry run pytest tests/acceptance -ra

.PHONY: test
test: test-unit test-integration ## Run all the tests

.PHONY: migration
migration: ## Generate a new migration, ex: make migration name=XXX
	poetry run alembic revision --autogenerate -m $(name)

.PHONY: pre-commit
pre-commit: check-lint check-format check-typing test-unit

.PHONY: pre-push
pre-push: test-integration
