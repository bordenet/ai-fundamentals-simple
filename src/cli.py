"""Command-line interface for documentation validation."""

import argparse
import logging
import sys
from pathlib import Path

from src.utils import LinkChecker, MarkdownValidator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


def validate_command(args: argparse.Namespace) -> int:
    """Run validation on markdown files.

    Args:
        args: Command-line arguments.

    Returns:
        Exit code (0 for success, 1 for errors found).
    """
    root_path = Path(args.path).resolve()

    if not root_path.exists():
        logger.error(f"Path does not exist: {root_path}")
        return 1

    if root_path.is_file():
        validator = MarkdownValidator(root_path.parent)
        errors = validator.validate_file(root_path)

        if errors:
            logger.error(f"Found {len(errors)} error(s):")
            for error in errors:
                print(f"  {error}")
            return 1

        logger.info("Validation passed")
        return 0

    # Directory validation
    checker = LinkChecker(root_path)
    results = checker.check_all_links()

    if results:
        total_errors = sum(len(errors) for errors in results.values())
        logger.error(f"Found {total_errors} error(s) in {len(results)} file(s):")

        for file_path, errors in sorted(results.items()):
            print(f"\n{file_path.relative_to(root_path)}:")
            for error in errors:
                print(f"  {error}")

        return 1

    logger.info("All validations passed")
    return 0


def main() -> int:
    """Run the CLI application.

    Returns:
        Exit code.
    """
    parser = argparse.ArgumentParser(
        description="Validate markdown documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate markdown files")
    validate_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to file or directory (default: current directory)",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if args.command == "validate":
        return validate_command(args)

    return 1


if __name__ == "__main__":
    sys.exit(main())
