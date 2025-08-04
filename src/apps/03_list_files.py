#!/usr/bin/env python3
"""
File Listing Agent - Step 3 of the Python AI Agent

This application adds directory listing capabilities to the file reading agent.
It demonstrates how to manage multiple tools and shows how tools can work together
to provide comprehensive file system access.

Key Learning Points:
- Managing multiple tools in a single agent
- Tool combination and workflow patterns
- Directory traversal and file system exploration
- Enhanced file information display

Usage:
    python src/apps/03_list_files.py
    python src/apps/03_list_files.py --verbose

Try asking:
    "List all files in this directory"
    "What files are in the examples directory and what's in fizzbuzz.js?"
    "Show me the directory structure and then read the riddle file"
"""

import sys
from pathlib import Path

import click

# Add src to path so we can import our modules
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from agent import Agent
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
    File listing and reading agent with Claude.

    This application demonstrates managing multiple tools that complement each other.
    The combination of list_files and read_file tools allows Claude to explore
    the file system and then examine specific files of interest.

    Key concepts demonstrated:
    - Multiple tool registration
    - Tool synergy and workflow patterns
    - File system navigation
    - Comprehensive error handling across tools
    """
    print("🤖 Python AI Agent - Step 3: File System Explorer")
    print("=" * 60)

    if verbose:
        print(
            "ℹ️  Verbose logging enabled - you'll see detailed API and tool interactions"
        )

    print("🔧 Tools available: read_file, list_files")
    print("💡 Try asking me to explore directories and read interesting files")
    print()

    # Create agent and add both tools
    agent = Agent(verbose=verbose)
    agent.add_tool(read_file_tool)
    agent.add_tool(list_files_tool)

    # Start the conversation loop
    agent.run()


if __name__ == "__main__":
    main()
