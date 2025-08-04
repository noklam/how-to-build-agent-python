#!/usr/bin/env python3
"""
Shell Command Agent - Step 4 of the Python AI Agent

This application adds shell command execution to the file system tools.
It demonstrates system integration capabilities and shows how to safely
execute external commands with proper error handling and output capture.

Key Learning Points:
- System integration through shell commands
- Command execution with timeout and error handling
- Output capture and formatting
- Security considerations for command execution

Usage:
    python src/apps/04_bash_tool.py
    python src/apps/04_bash_tool.py --verbose

Try asking:
    "Run git status"
    "List all .py files using bash"
    "Show me the current directory and then read the README"
    "Run ls -la and tell me about the files you see"
"""

import sys
from pathlib import Path

import click

# Add src to path so we can import our modules
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from agent import Agent
from tools.bash import bash_tool
from tools.list_files import list_files_tool
from tools.read_file import read_file_tool


@click.command()
@click.option(
    "--verbose",
    is_flag=True,
    help="Enable verbose logging to see detailed API interactions and tool execution",
)
def main(verbose: bool) -> None:
    """
    Shell command execution agent with Claude.

    This application demonstrates system integration by adding shell command
    execution capabilities. The bash tool allows Claude to interact with the
    operating system, run commands, and process their output.

    Key concepts demonstrated:
    - System integration through shell commands
    - Command execution with proper timeouts
    - Output capture and error handling
    - Combining file system and command-line tools
    """
    print("🤖 Python AI Agent - Step 4: System Integration")
    print("=" * 58)

    if verbose:
        print(
            "ℹ️  Verbose logging enabled - you'll see detailed API and tool interactions"
        )

    print("🔧 Tools available: read_file, list_files, safe_bash")
    print("💡 Try asking me to run safe shell commands and analyze their output")
    print("⚠️  Only read-only commands are allowed (ls, cat, grep, find, etc.)")
    print("🔒 Write operations, network commands, and system modifications are blocked")
    print()

    # Create agent and add all tools
    agent = Agent(verbose=verbose)
    agent.add_tool(read_file_tool)
    agent.add_tool(list_files_tool)
    agent.add_tool(bash_tool)

    # Start the conversation loop
    agent.run()


if __name__ == "__main__":
    main()
