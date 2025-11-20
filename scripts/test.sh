#!/bin/bash
# Test script - runs all tests and linting checks

set -e  # Exit on error

echo "================================"
echo "Running AI Fundamentals Tests"
echo "================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}Warning: No virtual environment detected${NC}"
    echo "Consider activating a virtual environment first"
    echo ""
fi

# Function to print section headers
print_section() {
    echo ""
    echo "================================"
    echo "$1"
    echo "================================"
}

# Check for Python files
PYTHON_FILES=$(find . -name "*.py" -not -path "./.venv/*" -not -path "./venv/*" -not -path "./env/*" -not -path "./.tox/*" -not -path "./build/*" -not -path "./dist/*" 2>/dev/null | wc -l)

if [ "$PYTHON_FILES" -eq 0 ]; then
    echo -e "${YELLOW}No Python files found to test${NC}"
    echo "This is primarily a documentation repository"
    echo -e "${GREEN}✓ Tests passed (no Python code to test)${NC}"
    exit 0
fi

# Run flake8
print_section "Running flake8 linter"
if command -v flake8 &> /dev/null; then
    flake8 . && echo -e "${GREEN}✓ flake8 passed${NC}" || { echo -e "${RED}✗ flake8 failed${NC}"; exit 1; }
else
    echo -e "${RED}✗ flake8 not installed${NC}"
    echo "Run: pip install -r requirements-dev.txt"
    exit 1
fi

# Run pytest if tests exist
print_section "Running pytest"
if [ -d "tests" ] && [ "$(find tests -name "test_*.py" 2>/dev/null | wc -l)" -gt 0 ]; then
    if command -v pytest &> /dev/null; then
        pytest tests/ -v --cov=. --cov-report=term-missing && echo -e "${GREEN}✓ pytest passed${NC}" || { echo -e "${RED}✗ pytest failed${NC}"; exit 1; }
    else
        echo -e "${YELLOW}pytest not installed, skipping tests${NC}"
    fi
else
    echo -e "${YELLOW}No tests directory or test files found, skipping pytest${NC}"
fi

# Run mypy if configured
print_section "Running mypy type checker"
if command -v mypy &> /dev/null; then
    if [ -f "pyproject.toml" ] || [ -f "mypy.ini" ]; then
        mypy . && echo -e "${GREEN}✓ mypy passed${NC}" || { echo -e "${RED}✗ mypy failed${NC}"; exit 1; }
    else
        echo -e "${YELLOW}mypy not configured, skipping${NC}"
    fi
else
    echo -e "${YELLOW}mypy not installed, skipping type checking${NC}"
fi

echo ""
echo "================================"
echo -e "${GREEN}All tests passed!${NC}"
echo "================================"
