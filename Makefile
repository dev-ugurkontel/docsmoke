.PHONY: help install format lint typecheck security test coverage build docker all clean

PYTHON ?= python3
VENV ?= .venv
BIN := $(VENV)/bin

help:
	@awk 'BEGIN {FS = ":.*##"; printf "Targets:\n"} /^[a-zA-Z_-]+:.*?##/ {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

$(BIN)/python:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip

install: $(BIN)/python ## Install project with dev extras
	$(BIN)/pip install -e ".[dev]"
	@if git config --get core.hooksPath >/dev/null; then \
		echo "Skipping pre-commit install because core.hooksPath is set."; \
	else \
		$(BIN)/pre-commit install; \
	fi

format: ## Auto-format the codebase
	$(BIN)/ruff format .
	$(BIN)/ruff check --fix .

lint: ## Run lint and format checks
	$(BIN)/ruff check .
	$(BIN)/ruff format --check .

typecheck: ## Run strict type checks
	$(BIN)/mypy src

security: ## Run bandit static analysis
	$(BIN)/bandit -q -r src -c pyproject.toml

test: ## Run the test suite
	$(BIN)/pytest

coverage: ## Run tests with HTML coverage report
	$(BIN)/pytest --cov-report=html

build: ## Build wheel and sdist
	$(BIN)/python -m pip install --upgrade build
	$(BIN)/python -m build

docker: ## Build docker image
	docker build -t docsmoke:local .

all: lint typecheck security test ## Run all quality gates

clean: ## Remove caches and build artifacts
	rm -rf .coverage .mypy_cache .pytest_cache .ruff_cache .venv build dist htmlcov coverage.xml src/*.egg-info src/**/__pycache__ tests/**/__pycache__
