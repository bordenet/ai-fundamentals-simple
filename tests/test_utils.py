"""Tests for utility functions."""

from src.utils import LinkChecker, MarkdownValidator


class TestMarkdownValidator:
    """Tests for MarkdownValidator class."""

    def test_init(self, tmp_path):
        """Test validator initialization."""
        validator = MarkdownValidator(tmp_path)
        assert validator.root_path == tmp_path

    def test_validate_nonexistent_file(self, tmp_path):
        """Test validation of nonexistent file."""
        validator = MarkdownValidator(tmp_path)
        errors = validator.validate_file(tmp_path / "nonexistent.md")
        assert len(errors) == 1
        assert "does not exist" in errors[0]

    def test_validate_valid_file(self, tmp_path):
        """Test validation of valid markdown file."""
        file_path = tmp_path / "test.md"
        file_path.write_text("# Title\n\n## Section\n\nContent here.\n")

        validator = MarkdownValidator(tmp_path)
        errors = validator.validate_file(file_path)
        assert len(errors) == 0

    def test_missing_h1(self, tmp_path):
        """Test detection of missing H1 header."""
        file_path = tmp_path / "test.md"
        file_path.write_text("## Section\n\nContent here.\n")

        validator = MarkdownValidator(tmp_path)
        errors = validator.validate_file(file_path)
        assert any("Missing H1" in error for error in errors)

    def test_multiple_h1(self, tmp_path):
        """Test detection of multiple H1 headers."""
        file_path = tmp_path / "test.md"
        file_path.write_text("# Title 1\n\n# Title 2\n")

        validator = MarkdownValidator(tmp_path)
        errors = validator.validate_file(file_path)
        assert any("Multiple H1" in error for error in errors)

    def test_header_hierarchy_skip(self, tmp_path):
        """Test detection of skipped header levels."""
        file_path = tmp_path / "test.md"
        file_path.write_text("# Title\n\n### Subsection\n")

        validator = MarkdownValidator(tmp_path)
        errors = validator.validate_file(file_path)
        assert any("Header level skipped" in error for error in errors)

    def test_broken_relative_link(self, tmp_path):
        """Test detection of broken relative links."""
        file_path = tmp_path / "test.md"
        file_path.write_text("# Title\n\n[Link](nonexistent.md)\n")

        validator = MarkdownValidator(tmp_path)
        errors = validator.validate_file(file_path)
        assert any("Broken link" in error for error in errors)

    def test_valid_relative_link(self, tmp_path):
        """Test validation of valid relative links."""
        target = tmp_path / "target.md"
        target.write_text("# Target\n")

        file_path = tmp_path / "test.md"
        file_path.write_text("# Title\n\n[Link](target.md)\n")

        validator = MarkdownValidator(tmp_path)
        errors = validator.validate_file(file_path)
        link_errors = [e for e in errors if "Broken link" in e]
        assert len(link_errors) == 0

    def test_external_links_ignored(self, tmp_path):
        """Test that external links are not validated."""
        file_path = tmp_path / "test.md"
        file_path.write_text(
            "# Title\n\n"
            "[HTTP](http://example.com)\n"
            "[HTTPS](https://example.com)\n"
            "[Email](mailto:test@example.com)\n"
        )

        validator = MarkdownValidator(tmp_path)
        errors = validator.validate_file(file_path)
        link_errors = [e for e in errors if "Broken link" in e]
        assert len(link_errors) == 0

    def test_anchor_links_ignored(self, tmp_path):
        """Test that anchor links are not validated."""
        file_path = tmp_path / "test.md"
        file_path.write_text("# Title\n\n[Anchor](#section)\n")

        validator = MarkdownValidator(tmp_path)
        errors = validator.validate_file(file_path)
        link_errors = [e for e in errors if "Broken link" in e]
        assert len(link_errors) == 0

    def test_unclosed_code_fence(self, tmp_path):
        """Test detection of unclosed code fences."""
        file_path = tmp_path / "test.md"
        file_path.write_text("# Title\n\n```python\ncode here\n")

        validator = MarkdownValidator(tmp_path)
        errors = validator.validate_file(file_path)
        assert any("Unclosed code fence" in error for error in errors)

    def test_valid_code_fence(self, tmp_path):
        """Test validation of properly closed code fences."""
        file_path = tmp_path / "test.md"
        file_path.write_text("# Title\n\n```python\ncode here\n```\n")

        validator = MarkdownValidator(tmp_path)
        errors = validator.validate_file(file_path)
        fence_errors = [e for e in errors if "code fence" in e]
        assert len(fence_errors) == 0

    def test_encoding_error(self, tmp_path):
        """Test handling of encoding errors."""
        file_path = tmp_path / "test.md"
        file_path.write_bytes(b"\xff\xfe")

        validator = MarkdownValidator(tmp_path)
        errors = validator.validate_file(file_path)
        assert any("Encoding error" in error for error in errors)


class TestLinkChecker:
    """Tests for LinkChecker class."""

    def test_init(self, tmp_path):
        """Test link checker initialization."""
        checker = LinkChecker(tmp_path)
        assert checker.root_path == tmp_path
        assert len(checker.all_files) == 0

    def test_scan_repository(self, tmp_path):
        """Test repository scanning."""
        (tmp_path / "file1.md").write_text("# File 1\n")
        (tmp_path / "file2.md").write_text("# File 2\n")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "file3.md").write_text("# File 3\n")

        checker = LinkChecker(tmp_path)
        checker.scan_repository()

        assert len(checker.all_files) == 3

    def test_check_all_links_no_errors(self, tmp_path):
        """Test checking links with no errors."""
        (tmp_path / "file1.md").write_text("# File 1\n\n[Link](file2.md)\n")
        (tmp_path / "file2.md").write_text("# File 2\n")

        checker = LinkChecker(tmp_path)
        results = checker.check_all_links()

        assert len(results) == 0

    def test_check_all_links_with_errors(self, tmp_path):
        """Test checking links with errors."""
        (tmp_path / "file1.md").write_text("# File 1\n\n[Link](nonexistent.md)\n")

        checker = LinkChecker(tmp_path)
        results = checker.check_all_links()

        assert len(results) == 1
        assert tmp_path / "file1.md" in results
