.PHONY: help install install-dev test lint format build clean pre-commit-install pre-commit-run

# Default target
help:
	@echo "AI Fundamentals - Development Commands"
	@echo ""
	@echo "Available targets:"
	@echo "  make install            - Install production dependencies"
	@echo "  make install-dev        - Install development dependencies"
	@echo "  make test               - Run tests and linting"
	@echo "  make lint               - Run flake8 linting only"
	@echo "  make format             - Format code with black and isort"
	@echo "  make build              - Run full build with quality checks"
	@echo "  make clean              - Remove build artifacts and cache files"
	@echo "  make pre-commit-install - Install pre-commit hooks"
	@echo "  make pre-commit-run     - Run pre-commit on all files"
	@echo "  make venv               - Create virtual environment"
	@echo ""

# Create virtual environment
venv:
	@echo "Creating virtual environment..."
	python3 -m venv .venv
	@echo "Virtual environment created at .venv"
	@echo "Activate it with: source .venv/bin/activate"

# Install production dependencies
install:
	pip install -r requirements.txt

# Install development dependencies
install-dev:
	pip install -r requirements-dev.txt

# Run tests and linting
test:
	@bash scripts/test.sh

# Run linting only
lint:
	@echo "Running flake8..."
	flake8 .

# Format code
format:
	@echo "Formatting code with black..."
	black --line-length 100 .
	@echo "Sorting imports with isort..."
	isort --profile black --line-length 100 .
	@echo "Code formatting complete!"

# Run full build
build:
	@bash scripts/build.sh

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".tox" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	rm -rf build/ dist/ 2>/dev/null || true
	@echo "Clean complete!"

# Install pre-commit hooks
pre-commit-install:
	@echo "Installing pre-commit hooks..."
	pre-commit install
	@echo "Pre-commit hooks installed!"

# Run pre-commit on all files
pre-commit-run:
	@echo "Running pre-commit on all files..."
	pre-commit run --all-files
