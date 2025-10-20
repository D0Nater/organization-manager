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

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  lint      - Run ruff and mypy checks"
	@echo "  style     - Check code formatting and import sorting"
	@echo "  format    - Automatically fix code style and formatting"
	@echo "  flint     - Format code and run linters"
