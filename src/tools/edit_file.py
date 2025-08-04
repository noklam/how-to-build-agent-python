"""File editing tool for the Python AI Agent."""

import logging
from pathlib import Path

from pydantic import BaseModel, Field, model_validator

from .base import BaseTool

logger = logging.getLogger(__name__)


class EditFileInput(BaseModel):
    """Input model for the edit_file tool."""

    path: str = Field(description="The path of the file to edit")
    old_str: str = Field(description="The string to be replaced in the file")
    new_str: str = Field(description="The string to replace old_str with")

    @model_validator(mode='after')
    def strings_must_be_different(self):
        """Ensure old_str and new_str are different."""
        if self.old_str == self.new_str:
            raise ValueError("old_str and new_str must be different")
        return self


class EditFileTool(BaseTool):
    """
    Tool for editing text files.

    This tool allows the agent to modify file contents by replacing strings.
    It's the final tool in the workshop progression, providing complete file
    manipulation capabilities.
    """

    name = "edit_file"
    description = (
        "Make edits to a text file. "
        "Replaces 'old_str' with 'new_str' in the given file. "
        "'old_str' and 'new_str' MUST be different from each other. "
        "If the file specified with path doesn't exist, it will be created."
    )
    input_model = EditFileInput

    def execute(self, input_data: EditFileInput) -> str:
        """
        Edit a file by replacing old_str with new_str.

        Args:
            input_data: Validated input with file path and replacement strings

        Returns:
            Success message or error description
        """
        file_path = Path(input_data.path)
        old_str = input_data.old_str
        new_str = input_data.new_str

        logger.info(f"Editing file: {file_path}")

        try:
            # Create parent directories if they don't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Read existing content or start with empty string for new files
            if file_path.exists():
                if not file_path.is_file():
                    error_msg = f"Path exists but is not a file: {file_path}"
                    logger.error(error_msg)
                    return error_msg

                try:
                    original_content = file_path.read_text(encoding="utf-8")
                except UnicodeDecodeError as e:
                    error_msg = f"Cannot decode file as UTF-8: {file_path} ({e})"
                    logger.error(error_msg)
                    return error_msg
            else:
                original_content = ""
                logger.info(f"Creating new file: {file_path}")

            # Perform replacement
            if old_str in original_content:
                # Count occurrences to inform user
                occurrence_count = original_content.count(old_str)

                # Check if replacement would be ambiguous (multiple occurrences)
                if occurrence_count > 1:
                    warning_msg = (
                        f"Warning: Found {occurrence_count} occurrences of the string. "
                        f"All will be replaced."
                    )
                    logger.warning(warning_msg)

                new_content = original_content.replace(old_str, new_str)

                # Write the modified content
                file_path.write_text(new_content, encoding="utf-8")

                success_msg = (
                    f"Successfully edited {file_path}. "
                    f"Replaced {occurrence_count} occurrence(s) of the specified string."
                )
                logger.info(success_msg)
                return success_msg

            else:
                # String not found - for new files, just write the new_str
                if not file_path.exists() and not old_str:
                    file_path.write_text(new_str, encoding="utf-8")
                    success_msg = f"Created new file: {file_path}"
                    logger.info(success_msg)
                    return success_msg
                else:
                    error_msg = f"String not found in file: '{old_str}'"
                    logger.error(error_msg)
                    return error_msg

        except PermissionError:
            error_msg = f"Permission denied writing to file: {file_path}"
            logger.error(error_msg)
            return error_msg

        except Exception as e:
            error_msg = f"Unexpected error editing file {file_path}: {e}"
            logger.error(error_msg)
            return error_msg


# Create tool instance for easy import
edit_file_tool = EditFileTool()
