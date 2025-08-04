"""File listing tool for the Python AI Agent."""

import logging
from pathlib import Path

from pydantic import BaseModel, Field

from .base import BaseTool

logger = logging.getLogger(__name__)


class ListFilesInput(BaseModel):
    """Input model for the list_files tool."""

    path: str | None = Field(
        default=".",
        description="The directory path to list. Defaults to current directory if not provided.",
    )


class ListFilesTool(BaseTool):
    """
    Tool for listing files and directories.

    This tool allows the agent to explore the file system by listing
    the contents of directories. It's the second tool in the workshop progression.
    """

    name = "list_files"
    description = (
        "List files and directories at a given path. "
        "If no path is provided, lists files in the current directory."
    )
    input_model = ListFilesInput

    def execute(self, input_data: ListFilesInput) -> str:
        """
        List files and directories in the specified path.

        Args:
            input_data: Validated input with directory path

        Returns:
            Formatted list of files and directories, or error message
        """
        dir_path = Path(input_data.path or ".")

        logger.info(f"Listing files in directory: {dir_path}")

        try:
            # Check if path exists
            if not dir_path.exists():
                error_msg = f"Directory not found: {dir_path}"
                logger.error(error_msg)
                return error_msg

            # Check if it's actually a directory
            if not dir_path.is_dir():
                error_msg = f"Path is not a directory: {dir_path}"
                logger.error(error_msg)
                return error_msg

            # Get directory contents
            entries = []

            try:
                for item in sorted(dir_path.iterdir()):
                    if item.is_dir():
                        entries.append(f"{item.name}/")
                    else:
                        # Show file size for regular files
                        size = item.stat().st_size
                        size_str = self._format_size(size)
                        entries.append(f"{item.name} ({size_str})")

            except PermissionError:
                error_msg = f"Permission denied accessing directory: {dir_path}"
                logger.error(error_msg)
                return error_msg

            if not entries:
                return f"Directory {dir_path} is empty"

            result = f"Contents of {dir_path}:\n" + "\n".join(entries)

            logger.info(f"Listed {len(entries)} items in {dir_path}")
            return result

        except Exception as e:
            error_msg = f"Unexpected error listing directory {dir_path}: {e}"
            logger.error(error_msg)
            return error_msg

    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format."""
        if size_bytes < 1024:
            return f"{size_bytes} bytes"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


# Create tool instance for easy import
list_files_tool = ListFilesTool()
