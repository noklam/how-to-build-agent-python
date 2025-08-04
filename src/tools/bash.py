"""Safe shell command execution tool for the Python AI Agent."""

import logging
import subprocess
from typing import ClassVar

from pydantic import BaseModel, Field

from .base import BaseTool

logger = logging.getLogger(__name__)


class BashInput(BaseModel):
    """Input model for the bash tool."""

    command: str = Field(description="The safe bash command to execute (read-only operations only)")


class SafeBashTool(BaseTool):
    """
    Tool for executing safe, read-only shell commands.

    This tool provides system integration capabilities while maintaining security
    by restricting commands to safe, read-only operations only.
    """

    name = "bash"
    description = (
        "Execute safe bash commands for read-only operations. "
        "Allowed commands include: ls, cat, grep, find, head, tail, wc, du, df, "
        "ps, pwd, whoami, date, echo, which, type, and basic pipes/redirections. "
        "Write operations, network commands, and system modifications are blocked."
    )
    input_model = BashInput
    
    # Whitelist of safe commands
    SAFE_COMMANDS: ClassVar[set[str]] = {
        'ls', 'cat', 'grep', 'find', 'head', 'tail', 'wc', 'du', 'df',
        'ps', 'pwd', 'whoami', 'date', 'echo', 'which', 'type', 'sort',
        'uniq', 'cut', 'awk', 'sed', 'tr', 'basename', 'dirname', 'file',
        'stat', 'realpath', 'readlink', 'uname', 'uptime', 'env', 'printenv'
    }

    # Dangerous patterns to block
    DANGEROUS_PATTERNS: ClassVar[set[str]] = {
        'rm', 'mv', 'cp', 'mkdir', 'rmdir', 'touch', 'chmod', 'chown',
        'sudo', 'su', 'passwd', 'useradd', 'userdel', 'mount', 'umount',
        'kill', 'killall', 'pkill', 'wget', 'curl', 'ssh', 'scp', 'rsync',
        'git', 'pip', 'npm', 'make', 'gcc', 'python', 'node', 'ruby',
        '>', '>>', 'tee', 'dd', 'fdisk', 'parted', 'mkfs', 'fsck'
    }

    def _validate_command_safety(self, command: str) -> str | None:
        """
        Validate that a command is safe to execute.
        
        Returns:
            Error message if unsafe, None if safe
        """
        # Convert to lowercase for case-insensitive matching
        command_lower = command.lower()
        
        # Check for dangerous patterns
        for pattern in self.DANGEROUS_PATTERNS:
            if pattern in command_lower:
                return f"Error: Command contains dangerous pattern '{pattern}' and is blocked for security"
        
        # Extract the first command (before pipes, etc.)
        first_command = command_lower.split()[0] if command_lower.split() else ""
        
        # Remove common prefixes
        if first_command.startswith('./') or first_command.startswith('/'):
            return "Error: Absolute paths and executable files are not allowed"
        
        # Check if the primary command is in our whitelist
        base_command = first_command.split('/')[-1]  # Get just the command name
        if base_command and base_command not in self.SAFE_COMMANDS:
            return f"Error: Command '{base_command}' is not in the whitelist of safe commands"
        
        return None

    def execute(self, input_data: BashInput) -> str:
        """
        Execute a safe bash command and return its output.

        Args:
            input_data: Validated input with command to execute

        Returns:
            Command output (stdout + stderr), or error message
        """
        command = input_data.command.strip()

        if not command:
            return "Error: Empty command provided"

        # Security validation
        security_error = self._validate_command_safety(command)
        if security_error:
            logger.warning(f"Blocked unsafe command: {command}")
            return security_error

        logger.info(f"Executing safe bash command: {command}")

        try:
            # Execute command with timeout and restricted environment
            result = subprocess.run(
                ["bash", "-c", command],
                capture_output=True,
                text=True,
                timeout=15,  # Shorter timeout for safety
                check=False,  # Don't raise exception on non-zero exit
                env={"PATH": "/usr/bin:/bin", "HOME": "/tmp"}  # Restricted environment
            )

            # Combine stdout and stderr
            output_parts = []

            if result.stdout:
                output_parts.append(f"STDOUT:\n{result.stdout}")

            if result.stderr:
                output_parts.append(f"STDERR:\n{result.stderr}")

            if not output_parts:
                output_parts.append("(No output)")

            # Add exit code information
            output = "\n".join(output_parts)
            if result.returncode != 0:
                output += f"\n\nExit code: {result.returncode}"

            logger.info(f"Command executed with exit code {result.returncode}")
            return output

        except subprocess.TimeoutExpired:
            error_msg = f"Command timed out after 15 seconds: {command}"
            logger.error(error_msg)
            return error_msg

        except FileNotFoundError:
            error_msg = "Bash not found. This tool requires bash to be installed."
            logger.error(error_msg)
            return error_msg

        except Exception as e:
            error_msg = f"Unexpected error executing command '{command}': {e}"
            logger.error(error_msg)
            return error_msg


# Create tool instance for easy import
bash_tool = SafeBashTool()
