"""Utility functions for AI Fundamentals documentation repository."""

import logging
import re
from pathlib import Path
from typing import Dict, List, Set

logger = logging.getLogger(__name__)


class MarkdownValidator:
    """Validates markdown files for common issues."""

    def __init__(self, root_path: Path):
        """Initialize validator.

        Args:
            root_path: Root directory of the repository.
        """
        self.root_path = Path(root_path)

    def validate_file(self, file_path: Path) -> List[str]:
        """Validate a single markdown file.

        Args:
            file_path: Path to markdown file.

        Returns:
            List of validation errors found.
        """
        errors = []

        if not file_path.exists():
            return [f"File does not exist: {file_path}"]

        try:
            content = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError as e:
            return [f"Encoding error in {file_path}: {e}"]

        errors.extend(self._check_headers(content, file_path))
        errors.extend(self._check_links(content, file_path))
        errors.extend(self._check_code_blocks(content, file_path))

        return errors

    def _check_headers(self, content: str, file_path: Path) -> List[str]:
        """Check header structure.

        Args:
            content: File content.
            file_path: Path to file.

        Returns:
            List of header-related errors.
        """
        errors = []
        lines = content.split("\n")

        # Check for title (H1)
        h1_count = sum(1 for line in lines if line.startswith("# "))
        if h1_count == 0:
            errors.append(f"{file_path}: Missing H1 title")
        elif h1_count > 1:
            errors.append(f"{file_path}: Multiple H1 headers found")

        # Check header hierarchy
        prev_level = 0
        for line_num, line in enumerate(lines, 1):
            if match := re.match(r"^(#{1,6})\s+", line):
                level = len(match.group(1))
                if level > prev_level + 1:
                    msg = f"{file_path}:{line_num}: " f"Header level skipped (from H{prev_level} to H{level})"
                    errors.append(msg)
                prev_level = level

        return errors

    def _check_links(self, content: str, file_path: Path) -> List[str]:
        """Check markdown links.

        Args:
            content: File content.
            file_path: Path to file.

        Returns:
            List of link-related errors.
        """
        errors = []

        # Find all markdown links [text](url)
        link_pattern = r"\[([^\]]+)\]\(([^)]+)\)"
        for match in re.finditer(link_pattern, content):
            url = match.group(2)

            # Skip external URLs
            if url.startswith(("http://", "https://", "mailto:")):
                continue

            # Skip anchors
            if url.startswith("#"):
                continue

            # Check relative file paths
            target_path = (file_path.parent / url).resolve()
            if not target_path.exists():
                errors.append(f"{file_path}: Broken link to {url}")

        return errors

    def _check_code_blocks(self, content: str, file_path: Path) -> List[str]:
        """Check code block formatting.

        Args:
            content: File content.
            file_path: Path to file.

        Returns:
            List of code block errors.
        """
        errors = []
        lines = content.split("\n")

        fence_count = 0
        for line in lines:
            if line.strip().startswith("```"):
                fence_count += 1

        if fence_count % 2 != 0:
            errors.append(f"{file_path}: Unclosed code fence")

        return errors


class LinkChecker:
    """Checks internal links across documentation."""

    def __init__(self, root_path: Path):
        """Initialize link checker.

        Args:
            root_path: Root directory of the repository.
        """
        self.root_path = Path(root_path)
        self.all_files: Set[Path] = set()

    def scan_repository(self) -> None:
        """Scan repository for all markdown files."""
        self.all_files = set(self.root_path.rglob("*.md"))
        logger.info(f"Found {len(self.all_files)} markdown files")

    def check_all_links(self) -> Dict[Path, List[str]]:
        """Check all internal links.

        Returns:
            Dictionary mapping file paths to lists of broken links.
        """
        if not self.all_files:
            self.scan_repository()

        results = {}
        validator = MarkdownValidator(self.root_path)

        for file_path in self.all_files:
            errors = validator.validate_file(file_path)
            if errors:
                results[file_path] = errors

        return results
