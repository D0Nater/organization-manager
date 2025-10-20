.PHONY: lint
lint:
	ruff check
	mypy --install-types --non-interactive --config-file setup.cfg .

.PHONY: style
style:
	ruff format --check --diff
	ruff check --diff .
	ruff check --diff . --select I

.PHONY: format
format:
	ruff format
	ruff check --fix .
	ruff check . --select I --fix

.PHONY: flint
flint: format lint

.PHONY: migration
migration:
	alembic revision --autogenerate -m "$(msg)"

.PHONY: dev-compose
dev-compose:
	docker compose -p orgmgr -f deployment/docker-compose.local.yml up -d --build --remove-orphans

.PHONY: dev-destroy
dev-destroy:
	docker compose -p orgmgr -f deployment/docker-compose.local.yml down -v --remove-orphans

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  lint      - Run ruff and mypy checks"
	@echo "  style     - Check code formatting and import sorting"
	@echo "  format    - Automatically fix code style and formatting"
	@echo "  flint     - Format code and run linters"
	@echo "  migration - Create a new Alembic migration (use msg='')"
	@echo "  dev-compose  - Start local development environment"
	@echo "  dev-destroy  - Remove local development environment"
