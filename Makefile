# ==============================================================================
# Makefile for django-clickify
#
# Usage:
#   make help       Show this help message.
#   make install    Install dependencies.
#   make format     Format code and auto-fix linting errors.
#   make check      Check for linting and formatting errors.
#   make test       Run the test suite.
#   make precommit  Install pre-commit hooks.
# ==============================================================================

.DEFAULT_GOAL := help
.PHONY: help install format check test precommit

# Help command
help: ## Show this help message.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Install dependencies with Poetry
install: ## Install project dependencies
	@poetry install

# Format code and auto-fix linting issues
format: ## Format code and fix linting
	@echo "Formatting code..."
	@poetry run ruff check . --fix

# Check for linting/formatting issues without fixing
check: ## Check code formatting and linting
	@echo "Checking code style..."
	@poetry run ruff check .

# Run tests using pytest
test: ## Run the test suite
	@echo "Running tests..."
	@poetry run pytest

# Install pre-commit hooks
precommit: ## Install pre-commit hooks
	@echo "Installing pre-commit if not already installed..."
	@poetry add --group dev pre-commit || true
	@echo "Installing Git hooks..."
	@poetry run pre-commit install
	@echo "Pre-commit hooks installed!"
