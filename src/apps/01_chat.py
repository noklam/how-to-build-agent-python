#!/usr/bin/env python3
"""
Basic Chat Application - Step 1 of the Python AI Agent

This is the foundation application that demonstrates a simple chat interface
with Claude. It establishes the core conversation pattern without any tools.

Key Learning Points:
- Basic conversation loop with Claude API
- User input handling and display formatting
- Verbose logging for debugging
- Agent initialization and configuration

Usage:
    python src/apps/01_chat.py
    python src/apps/01_chat.py --verbose
"""

import sys
from pathlib import Path

import click

# Add src to path so we can import our modules
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from agent import Agent


@click.command()
@click.option(
    "--verbose",
    is_flag=True,
    help="Enable verbose logging to see detailed API interactions",
)
def main(verbose: bool) -> None:
    """
    Basic chat application with Claude.

    This application demonstrates the fundamental conversation loop that all
    other applications in this workshop build upon. It shows how to:

    - Initialize an Agent instance
    - Start an interactive chat session
    - Handle user input and Claude responses
    - Use verbose logging for debugging

    The agent has no tools at this stage - it can only engage in conversation.
    """
    print("🤖 Python AI Agent - Step 1: Basic Chat")
    print("=" * 50)

    if verbose:
        print("ℹ️  Verbose logging enabled - you'll see detailed API interactions")

    print("💡 This agent can only chat - no tools available yet")
    print()

    # Create agent with no tools
    agent = Agent(verbose=verbose)

    # Start the conversation loop
    agent.run()


if __name__ == "__main__":
    main()
