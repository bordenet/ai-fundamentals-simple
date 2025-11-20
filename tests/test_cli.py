"""Tests for CLI module."""

import sys
from unittest.mock import patch

from src.cli import main, validate_command


class TestValidateCommand:
    """Tests for validate command."""

    def test_validate_nonexistent_path(self, tmp_path, caplog):
        """Test validation of nonexistent path."""
        args = type("Args", (), {"path": str(tmp_path / "nonexistent")})()

        exit_code = validate_command(args)

        assert exit_code == 1
        assert "does not exist" in caplog.text.lower()

    def test_validate_single_file_success(self, tmp_path):
        """Test successful validation of single file."""
        file_path = tmp_path / "test.md"
        file_path.write_text("# Title\n\n## Section\n\nContent.\n")

        args = type("Args", (), {"path": str(file_path)})()
        exit_code = validate_command(args)

        assert exit_code == 0

    def test_validate_single_file_with_errors(self, tmp_path, caplog):
        """Test validation of single file with errors."""
        file_path = tmp_path / "test.md"
        file_path.write_text("## Section\n\nNo H1 header.\n")

        args = type("Args", (), {"path": str(file_path)})()
        exit_code = validate_command(args)

        assert exit_code == 1
        assert "error" in caplog.text.lower()

    def test_validate_directory_success(self, tmp_path):
        """Test successful validation of directory."""
        (tmp_path / "file1.md").write_text("# File 1\n")
        (tmp_path / "file2.md").write_text("# File 2\n")

        args = type("Args", (), {"path": str(tmp_path)})()
        exit_code = validate_command(args)

        assert exit_code == 0

    def test_validate_directory_with_errors(self, tmp_path, caplog):
        """Test validation of directory with errors."""
        (tmp_path / "file1.md").write_text("# File 1\n\n[Link](missing.md)\n")

        args = type("Args", (), {"path": str(tmp_path)})()
        exit_code = validate_command(args)

        assert exit_code == 1
        assert "error" in caplog.text.lower()


class TestMain:
    """Tests for main function."""

    def test_main_no_command(self, capsys):
        """Test main with no command."""
        with patch.object(sys, "argv", ["cli.py"]):
            exit_code = main()

        assert exit_code == 1

    def test_main_validate_command(self, tmp_path):
        """Test main with validate command."""
        file_path = tmp_path / "test.md"
        file_path.write_text("# Title\n")

        with patch.object(sys, "argv", ["cli.py", "validate", str(file_path)]):
            exit_code = main()

        assert exit_code == 0

    def test_main_validate_default_path(self, tmp_path, monkeypatch):
        """Test main with validate command and default path."""
        monkeypatch.chdir(tmp_path)
        (tmp_path / "test.md").write_text("# Title\n")

        with patch.object(sys, "argv", ["cli.py", "validate"]):
            exit_code = main()

        assert exit_code == 0

    def test_main_validate_with_errors(self, tmp_path):
        """Test main with validate command and errors."""
        file_path = tmp_path / "test.md"
        file_path.write_text("## No H1\n")

        with patch.object(sys, "argv", ["cli.py", "validate", str(file_path)]):
            exit_code = main()

        assert exit_code == 1
