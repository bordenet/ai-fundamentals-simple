"""Utility functions for AI Fundamentals project."""


def validate_document_structure(document: str) -> bool:
    """Validate the structure of a document.

    Args:
        document: The document content to validate.

    Returns:
        True if the document structure is valid, False otherwise.
    """
    if not document:
        return False

    # Check for basic structure
    required_sections = ["Overview", "Prerequisites"]
    for section in required_sections:
        if section not in document:
            return False

    return True


def format_learning_checkpoint(checkpoint: dict) -> str:
    """Format a learning checkpoint for display.

    Args:
        checkpoint: Dictionary containing checkpoint information with keys
            'title', 'description', and 'completed'.

    Returns:
        Formatted checkpoint string.
    """
    status = "✓" if checkpoint.get("completed", False) else "☐"
    title = checkpoint.get("title", "Untitled")
    description = checkpoint.get("description", "")

    formatted = f"{status} {title}"
    if description:
        formatted += f"\n  {description}"

    return formatted


def calculate_progress(completed_items: int, total_items: int) -> float:
    """Calculate progress percentage.

    Args:
        completed_items: Number of completed items.
        total_items: Total number of items.

    Returns:
        Progress as a percentage (0-100).

    Raises:
        ValueError: If total_items is zero or negative.
    """
    if total_items <= 0:
        raise ValueError("Total items must be greater than zero")

    return (completed_items / total_items) * 100
