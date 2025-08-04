"""Core Agent class for the Python AI agent workshop."""

import logging
import sys
from typing import Any, Callable, Dict, List, Optional, Protocol

import anthropic
from rich.console import Console
from rich.logging import RichHandler
from rich.text import Text


class Tool(Protocol):
    """Protocol defining the interface for agent tools."""
    
    name: str
    description: str
    
    def __call__(self, **kwargs: Any) -> str:
        """Execute the tool with the given arguments."""
        ...
    
    def get_schema(self) -> Dict[str, Any]:
        """Return the JSON schema for the tool's input parameters."""
        ...


class Agent:
    """
    AI agent that can engage in conversations and use tools.
    
    This is the core agent class used across all workshop applications.
    It handles the conversation loop, tool execution, and interaction with
    the Anthropic Claude API.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        verbose: bool = False,
        get_user_input: Optional[Callable[[], str]] = None
    ):
        """
        Initialize the agent.
        
        Args:
            api_key: Anthropic API key (will use environment variable if not provided)
            verbose: Enable verbose logging
            get_user_input: Function to get user input (defaults to input())
        """
        self.verbose = verbose
        self.tools: Dict[str, Tool] = {}
        self.conversation: List[anthropic.MessageParam] = []
        self.console = Console()
        
        # Setup logging
        self._setup_logging()
        
        # Initialize Anthropic client
        self.client = anthropic.Anthropic(api_key=api_key)
        if self.verbose:
            self.logger.info("Anthropic client initialized")
        
        # Set up user input function
        self.get_user_input = get_user_input or self._default_input
        
    def _setup_logging(self) -> None:
        """Configure logging based on verbose setting."""
        if self.verbose:
            logging.basicConfig(
                level=logging.INFO,
                format="%(message)s",
                handlers=[RichHandler(console=self.console, show_time=True)]
            )
        else:
            logging.basicConfig(level=logging.WARNING)
        
        self.logger = logging.getLogger(__name__)
        
    def _default_input(self) -> str:
        """Default user input function."""
        try:
            return input()
        except (EOFError, KeyboardInterrupt):
            return ""
    
    def add_tool(self, tool: Tool) -> None:
        """
        Add a tool to the agent's toolkit.
        
        Args:
            tool: Tool instance to add
        """
        self.tools[tool.name] = tool
        if self.verbose:
            self.logger.info(f"Added tool: {tool.name}")
    
    def run(self) -> None:
        """
        Run the main conversation loop.
        
        This method handles the interactive chat session, processing user input,
        calling Claude, executing tools, and displaying responses.
        """
        if self.verbose:
            self.logger.info(f"Starting chat session with {len(self.tools)} tools enabled")
        
        self.console.print("Chat with Claude (use 'ctrl-c' to quit)", style="bold blue")
        
        try:
            while True:
                # Get user input
                self.console.print("You: ", style="bold blue", end="")
                user_input = self.get_user_input()
                
                if not user_input.strip():
                    if self.verbose:
                        self.logger.info("Skipping empty message")
                    continue
                
                if self.verbose:
                    self.logger.info(f"User input received: {user_input!r}")
                
                # Add user message to conversation
                user_message = anthropic.MessageParam(
                    role="user",
                    content=user_input
                )
                self.conversation.append(user_message)
                
                # Process the conversation with Claude
                self._process_conversation()
                
        except (EOFError, KeyboardInterrupt):
            if self.verbose:
                self.logger.info("Chat session ended by user")
            self.console.print("\nGoodbye!", style="bold blue")
    
    def _process_conversation(self) -> None:
        """Process the current conversation with Claude, handling tool calls."""
        if self.verbose:
            self.logger.info(f"Sending message to Claude, conversation length: {len(self.conversation)}")
        
        # Make API call to Claude
        try:
            message = self._call_claude()
            self.conversation.append(message.to_param())
        except Exception as e:
            self.console.print(f"Error calling Claude: {e}", style="bold red")
            return
        
        # Process Claude's response, handling any tool calls
        while True:
            tool_results = []
            has_tool_use = False
            
            if self.verbose:
                self.logger.info(f"Processing {len(message.content)} content blocks from Claude")
            
            for content in message.content:
                if content.type == "text":
                    # Display Claude's text response
                    self.console.print("Claude: ", style="bold yellow", end="")
                    self.console.print(content.text)
                    
                elif content.type == "tool_use":
                    has_tool_use = True
                    tool_use = content
                    
                    if self.verbose:
                        self.logger.info(f"Tool use detected: {tool_use.name}")
                    
                    # Display tool call
                    self.console.print("tool: ", style="bold cyan", end="")
                    self.console.print(f"{tool_use.name}({tool_use.input})")
                    
                    # Execute the tool
                    result = self._execute_tool(tool_use.name, tool_use.input)
                    
                    # Display result
                    self.console.print("result: ", style="bold green", end="")
                    self.console.print(result)
                    
                    # Add tool result for next Claude call
                    tool_results.append(
                        anthropic.ContentBlockParam(
                            type="tool_result",
                            tool_use_id=tool_use.id,
                            content=result
                        )
                    )
            
            # If no tools were used, we're done
            if not has_tool_use:
                break
            
            # Send tool results back to Claude
            if tool_results:
                tool_message = anthropic.MessageParam(
                    role="user",
                    content=tool_results
                )
                self.conversation.append(tool_message)
                
                if self.verbose:
                    self.logger.info("Sending tool results back to Claude")
                
                try:
                    message = self._call_claude()
                    self.conversation.append(message.to_param())
                except Exception as e:
                    self.console.print(f"Error calling Claude: {e}", style="bold red")
                    break
    
    def _call_claude(self) -> anthropic.Message:
        """Make an API call to Claude."""
        # Prepare tools for API call
        anthropic_tools = []
        for tool in self.tools.values():
            anthropic_tools.append(
                anthropic.ToolParam(
                    name=tool.name,
                    description=tool.description,
                    input_schema=tool.get_schema()
                )
            )
        
        if self.verbose:
            self.logger.info(f"Making API call with {len(anthropic_tools)} tools")
        
        # Make the API call
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=self.conversation,
            tools=anthropic_tools if anthropic_tools else None
        )
        
        if self.verbose:
            self.logger.info("API call successful")
        
        return response
    
    def _execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """Execute a tool and return its result."""
        if tool_name not in self.tools:
            error_msg = f"Tool '{tool_name}' not found"
            if self.verbose:
                self.logger.error(error_msg)
            return error_msg
        
        tool = self.tools[tool_name]
        
        try:
            if self.verbose:
                self.logger.info(f"Executing tool: {tool_name}")
            
            # Execute the tool
            result = tool(**tool_input)
            
            if self.verbose:
                self.logger.info(f"Tool {tool_name} executed successfully")
            
            return result
            
        except Exception as e:
            error_msg = f"Error executing tool {tool_name}: {e}"
            if self.verbose:
                self.logger.error(error_msg)
            return error_msg