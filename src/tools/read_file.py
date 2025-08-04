"""File reading tool for the Python AI Agent."""

import logging
from pathlib import Path

from pydantic import BaseModel, Field

from .base import BaseTool

logger = logging.getLogger(__name__)


class ReadFileInput(BaseModel):
    """Input model for the read_file tool."""

    path: str = Field(
        description="The relative path of a file in the working directory"
    )


class ReadFileTool(BaseTool):
    """
    Tool for reading file contents.

    This tool allows the agent to read text files from the file system.
    It's the first tool introduced in the workshop progression.
    """

    name = "read_file"
    description = (
        "Read the contents of a given relative file path. "
        "Use this when you want to see what's inside a file. "
        "Do not use this with directory names."
    )
    input_model = ReadFileInput

    def execute(self, input_data: ReadFileInput) -> str:
        """
        Read and return the contents of a file.

        Args:
            input_data: Validated input with file path

        Returns:
            File contents as a string, or error message if file cannot be read
        """
        file_path = Path(input_data.path)

        logger.info(f"Reading file: {file_path}")

        try:
            # Check if file exists
            if not file_path.exists():
                error_msg = f"File not found: {file_path}"
                logger.error(error_msg)
                return error_msg

            # Check if it's actually a file (not a directory)
            if not file_path.is_file():
                error_msg = f"Path is not a file: {file_path}"
                logger.error(error_msg)
                return error_msg

            # Read file contents
            content = file_path.read_text(encoding="utf-8")

            logger.info(f"Successfully read {len(content)} characters from {file_path}")
            return content

        except PermissionError:
            error_msg = f"Permission denied reading file: {file_path}"
            logger.error(error_msg)
            return error_msg

        except UnicodeDecodeError as e:
            error_msg = f"Cannot decode file as UTF-8: {file_path} ({e})"
            logger.error(error_msg)
            return error_msg

        except Exception as e:
            error_msg = f"Unexpected error reading file {file_path}: {e}"
            logger.error(error_msg)
            return error_msg


# Create tool instance for easy import
read_file_tool = ReadFileTool()
