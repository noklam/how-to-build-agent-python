#!/usr/bin/env python3
"""
Complete File Editor Agent - Step 5 of the Python AI Agent

This is the final and most capable agent in the workshop progression.
It includes all previous tools plus file editing capabilities, making it
a fully functional agent that can read, explore, execute commands, and
modify files in the file system.

Key Learning Points:
- Complete agent capabilities with all tools
- File modification with validation and safety checks
- String replacement with ambiguity handling
- Directory creation and file management
- Comprehensive agent workflows

Usage:
    python src/apps/05_edit_tool.py
    python src/apps/05_edit_tool.py --verbose

Try asking:
    "Create a simple Python hello world script"
    "Add a comment to the top of examples/fizzbuzz.js"
    "List files, read one, and make an improvement to it"
    "Create a new file with some content and then read it back"
"""

import sys
from pathlib import Path

import click

# Add src to path so we can import our modules
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from agent import Agent
from tools.bash import bash_tool
from tools.edit_file import edit_file_tool
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
    Complete file editing agent with Claude.

    This is the most capable agent in the workshop, featuring all four tools:
    - read_file: Read file contents
    - list_files: Explore directory structure
    - bash: Execute shell commands
    - edit_file: Modify or create files

    This agent can perform complete development workflows, from exploring
    a codebase to making modifications and running commands.

    Key concepts demonstrated:
    - Full agent capabilities with comprehensive toolset
    - File modification with safety validations
    - Complete development workflow support
    - Tool synergy across all four capabilities
    """
    print("🤖 Python AI Agent - Step 5: Complete Agent")
    print("=" * 55)

    if verbose:
        print(
            "ℹ️  Verbose logging enabled - you'll see detailed API and tool interactions"
        )

    print("🔧 Tools available: read_file, list_files, bash, edit_file")
    print("💡 This agent can explore, read, execute commands, and edit files")
    print("⚠️  File edits create directories as needed and validate all changes")
    print()

    # Create agent and add all tools
    agent = Agent(verbose=verbose)
    agent.add_tool(read_file_tool)
    agent.add_tool(list_files_tool)
    agent.add_tool(bash_tool)
    agent.add_tool(edit_file_tool)

    # Start the conversation loop
    agent.run()


if __name__ == "__main__":
    main()
