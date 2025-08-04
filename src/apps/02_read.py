#!/usr/bin/env python3
"""
File Reading Agent - Step 2 of the Python AI Agent

This application builds on the basic chat by adding the first tool: file reading.
It demonstrates how to integrate tools with the agent and shows the tool execution
pattern that all subsequent applications follow.

Key Learning Points:
- Adding tools to an agent
- Tool definition and schema generation
- Tool execution and result handling
- File system operations with error handling

Usage:
    python src/apps/02_read.py
    python src/apps/02_read.py --verbose

Try asking:
    "Read the contents of examples/riddle.txt"
    "What's in the examples/fizzbuzz.js file?"
"""

import sys
from pathlib import Path

import click

# Add src to path so we can import our modules
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from agent import Agent
from tools.read_file import read_file_tool


@click.command()
@click.option(
    "--verbose",
    is_flag=True,
    help="Enable verbose logging to see detailed API interactions and tool execution",
)
def main(verbose: bool) -> None:
    """
    File reading agent with Claude.

    This application demonstrates how to add the first tool to an agent.
    The read_file tool allows Claude to read and analyze file contents,
    opening up many new possibilities for interaction.

    Key concepts demonstrated:
    - Tool registration with agent.add_tool()
    - Automatic JSON schema generation from Pydantic models
    - Error handling in tool execution
    - File path validation and security
    """
    print("🤖 Python AI Agent - Step 2: File Reading")
    print("=" * 55)

    if verbose:
        print(
            "ℹ️  Verbose logging enabled - you'll see detailed API and tool interactions"
        )

    print("🔧 Tools available: read_file")
    print("💡 Try asking me to read files in the examples/ directory")
    print()

    # Create agent and add the read_file tool
    agent = Agent(verbose=verbose)
    agent.add_tool(read_file_tool)

    # Start the conversation loop
    agent.run()


if __name__ == "__main__":
    main()
