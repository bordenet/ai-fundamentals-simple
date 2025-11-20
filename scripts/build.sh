#!/bin/bash
# Build script - runs quality checks and prepares for deployment

set -e  # Exit on error

echo "================================"
echo "Building AI Fundamentals"
echo "================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print section headers
print_section() {
    echo ""
    echo "================================"
    echo "$1"
    echo "================================"
}

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}Warning: No virtual environment detected${NC}"
    echo "Consider activating a virtual environment first"
    echo ""
fi

# Install/update dependencies
print_section "Installing dependencies"
if [ -f "requirements-dev.txt" ]; then
    pip install -q -r requirements-dev.txt && echo -e "${GREEN}✓ Dependencies installed${NC}" || { echo -e "${RED}✗ Failed to install dependencies${NC}"; exit 1; }
else
    echo -e "${RED}✗ requirements-dev.txt not found${NC}"
    exit 1
fi

# Run code formatting checks
print_section "Checking code formatting"
if command -v black &> /dev/null; then
    black --check --line-length 100 . && echo -e "${GREEN}✓ Code formatting check passed${NC}" || { echo -e "${YELLOW}! Code needs formatting (run: black .)${NC}"; }
else
    echo -e "${YELLOW}black not installed, skipping formatting check${NC}"
fi

# Run import sorting checks
print_section "Checking import sorting"
if command -v isort &> /dev/null; then
    isort --check-only --profile black --line-length 100 . && echo -e "${GREEN}✓ Import sorting check passed${NC}" || { echo -e "${YELLOW}! Imports need sorting (run: isort .)${NC}"; }
else
    echo -e "${YELLOW}isort not installed, skipping import check${NC}"
fi

# Run linting
print_section "Running linting checks"
bash scripts/test.sh || { echo -e "${RED}✗ Tests failed${NC}"; exit 1; }

# Check for common issues
print_section "Running additional checks"

# Check for TODO/FIXME comments
TODO_COUNT=$(grep -r "TODO\|FIXME" --include="*.py" . 2>/dev/null | wc -l || echo "0")
if [ "$TODO_COUNT" -gt 0 ]; then
    echo -e "${YELLOW}Found $TODO_COUNT TODO/FIXME comments${NC}"
fi

# Check for print statements (should use logging)
PRINT_COUNT=$(grep -r "print(" --include="*.py" . 2>/dev/null | grep -v "# noqa" | wc -l || echo "0")
if [ "$PRINT_COUNT" -gt 0 ]; then
    echo -e "${YELLOW}Found $PRINT_COUNT print() statements (consider using logging)${NC}"
fi

# Verify documentation exists
if [ ! -f "README.md" ]; then
    echo -e "${RED}✗ README.md not found${NC}"
    exit 1
else
    echo -e "${GREEN}✓ README.md exists${NC}"
fi

echo ""
echo "================================"
echo -e "${GREEN}Build completed successfully!${NC}"
echo "================================"
echo ""
echo "Next steps:"
echo "  - Review any warnings above"
echo "  - Run 'git status' to see changes"
echo "  - Commit and push when ready"
