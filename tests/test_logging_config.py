"""Tests for logging configuration."""

import logging

from src.logging_config import configure_logging


class TestLoggingConfig:
    """Tests for logging configuration."""

    def test_configure_logging_default_level(self):
        """Test logging configuration with default level."""
        configure_logging()

        logger = logging.getLogger("src")
        assert logger.level == logging.INFO

    def test_configure_logging_debug_level(self):
        """Test logging configuration with DEBUG level."""
        configure_logging(level="DEBUG")

        logger = logging.getLogger("src")
        assert logger.level == logging.DEBUG

    def test_configure_logging_warning_level(self):
        """Test logging configuration with WARNING level."""
        configure_logging(level="WARNING")

        logger = logging.getLogger("src")
        assert logger.level == logging.WARNING

    def test_configure_logging_error_level(self):
        """Test logging configuration with ERROR level."""
        configure_logging(level="ERROR")

        logger = logging.getLogger("src")
        assert logger.level == logging.ERROR

    def test_logging_has_handlers(self):
        """Test that logging configuration adds handlers."""
        configure_logging(level="INFO")

        logger = logging.getLogger("src")
        assert len(logger.handlers) > 0
