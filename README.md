# Python AI Agent

A hands-on workshop for learning how to build AI agents with progressively increasing capabilities using Python. This repository contains five different agent implementations that demonstrate the evolution from a simple chat interface to a fully capable agent with file system access and tool execution.

This is the Python version of the Go-based agent workshop, redesigned to leverage Python's strengths while maintaining the same educational progression.

## 🎯 Learning Objectives

By working through this workshop, you will learn:

- How to integrate with the Anthropic Claude API using Python
- Modern Python patterns for building AI agents (Pydantic, Click, Rich)
- The fundamentals of tool-calling and function execution
- How to build a robust agent event loop
- Progressive enhancement of agent capabilities
- Error handling and logging in agent systems
- Pythonic approaches to schema generation and validation

## 🏗️ Architecture Overview

All applications share a common architecture pattern with a central event loop that handles user input, sends messages to Claude, processes tool calls, and returns results.

### Core Components

**Agent Class (`src/agent.py`)**:
- Handles conversation loop and API interactions
- Manages tool registry and execution
- Provides rich console output and logging
- Supports verbose debugging mode

**Tool System (`src/tools/`)**:
- Protocol-based tool interface using Pydantic
- Automatic JSON schema generation
- Built-in input validation and error handling
- Consistent logging and result formatting

**Progressive Applications (`src/apps/`)**:
- Numbered files showing clear learning progression
- Each builds upon the previous with additional capabilities
- Comprehensive documentation and usage examples

## 📚 Application Progression

The workshop follows a numbered progression through five applications:

### 1. Basic Chat (`01_chat.py`)
**Purpose**: Establish the foundation - a simple chat interface with Claude

**Features**:
- Basic conversation loop with rich console output
- User input handling with graceful interruption support
- API integration with Anthropic Claude
- Verbose logging with Rich formatting

**Usage**:
```bash
python src/apps/01_chat.py
python src/apps/01_chat.py --verbose
```

### 2. File Reading Agent (`02_read.py`)
**Purpose**: Add the first tool - file reading capability

**Features**:
- Everything from `01_chat.py`
- `read_file` tool with Pydantic validation
- Automatic schema generation and tool registration
- Comprehensive file error handling

**Usage**:
```bash
python src/apps/02_read.py
# Try: "Read the contents of examples/fizzbuzz.js"
```

### 3. File Listing Agent (`03_list_files.py`)
**Purpose**: Expand file system access with directory listing

**Features**:
- Everything from `02_read.py`
- `list_files` tool for directory exploration
- File size formatting and directory indicators
- Multiple tool coordination

**Usage**:
```bash
python src/apps/03_list_files.py
# Try: "List all files in this directory"
# Try: "What files are available and what's in fizzbuzz.js?"
```

### 4. Shell Command Agent (`04_bash_tool.py`)
**Purpose**: Add shell command execution capabilities

**Features**:
- Everything from `03_list_files.py`
- `bash` tool for executing shell commands
- Command timeout and output capture
- Separate stdout/stderr handling

**Usage**:
```bash
python src/apps/04_bash_tool.py
# Try: "Run git status"
# Try: "List all .py files using bash"
```

### 5. Complete File Editor (`05_edit_tool.py`)
**Purpose**: Complete agent with file modification capabilities

**Features**:
- Everything from `04_bash_tool.py`
- `edit_file` tool for modifying and creating files
- String replacement with validation
- Automatic directory creation

**Usage**:
```bash
python src/apps/05_edit_tool.py
# Try: "Create a simple Python hello world script"
# Try: "Add a comment to the top of examples/fizzbuzz.js"
```

## 🚀 Setup

### Prerequisites
- Python 3.9+ (recommended: Python 3.11+)
- Anthropic API key

### Installation

1. **Clone and navigate to the Python version**:
```bash
cd python-agents
```

2. **Install dependencies**:
```bash
# Using pip
pip install -r requirements.txt

# Or using pip with development dependencies
pip install -e ".[dev]"

# Or using poetry (if you prefer)
poetry install
```

3. **Set up your API key**:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

## 📖 Usage Examples

### Basic Chat
```bash
$ python src/apps/01_chat.py
🤖 Python AI Agent - Step 1: Basic Chat
==================================================
💡 This agent can only chat - no tools available yet

Chat with Claude (use 'ctrl-c' to quit)
You: Hello!
Claude: Hello! How can I help you today?
```

### File Operations
```bash
$ python src/apps/05_edit_tool.py
🤖 Python AI Agent - Step 5: Complete Agent
=======================================================
🔧 Tools available: read_file, list_files, bash, edit_file

You: What files are in the examples directory?
tool: list_files({"path": "examples"})
result: Contents of examples:
fizzbuzz.js (527 bytes)
riddle.txt (108 bytes)
Claude: I can see there are two files in the examples directory...

You: Read the riddle file
tool: read_file({"path": "examples/riddle.txt"})
result: I have a mane but I'm not a lion...
Claude: This is a riddle! The answer is "a horse"...
```

### Debugging with Verbose Mode
```bash
$ python src/apps/05_edit_tool.py --verbose
# Provides detailed logging of:
# - API calls and responses
# - Tool execution details
# - File operations and validation
# - Error traces with Rich formatting
```

## 🧪 Test Files

The repository includes sample files for testing in the `examples/` directory:

- **`fizzbuzz.js`**: A JavaScript FizzBuzz implementation for reading/editing
- **`riddle.txt`**: A simple riddle for content analysis


### Project Structure
- **`src/agent.py`**: Core Agent class with conversation loop
- **`src/tools/`**: Tool implementations with Pydantic models
- **`src/apps/`**: Progressive application examples (01-05)
- **`examples/`**: Sample files for testing
- **`pyproject.toml`**: Modern Python packaging configuration

## 🎓 Workshop Flow

### Phase 1: Understanding the Basics (Steps 1-2)
1. Start with `01_chat.py` to understand the conversation loop
2. Examine the Agent class and Rich console integration
3. Move to `02_read.py` to see tool integration
4. Understand Pydantic validation and schema generation

### Phase 2: Building Complexity (Steps 3-4)
1. Explore `03_list_files.py` for multiple tool management
2. Test directory traversal and file system operations
3. Use `04_bash_tool.py` to see command execution
4. Learn about timeout handling and output capture

### Phase 3: Complete Agent (Step 5)
1. Master `05_edit_tool.py` for complete file operations
2. Understand validation and safety measures
3. Build complete agent workflows
4. Experiment with tool combinations

## 🔍 Key Python Improvements Over Go Version

### Modern Python Patterns
- **Pydantic models** for automatic validation and schema generation
- **Rich console** for beautiful output formatting
- **Click** for elegant CLI argument handling
- **Protocol-based interfaces** for type safety
- **Comprehensive error handling** with custom exceptions

### Simplified Architecture
- **Single Agent class** shared across all applications
- **Automatic tool discovery** and registration
- **Built-in JSON handling** without manual parsing
- **Pythonic error patterns** with proper exception hierarchy
- **Dynamic imports** instead of static tool arrays

### Enhanced Developer Experience
- **Type hints** throughout for better IDE support
- **Verbose logging** with Rich formatting
- **Clear progression** with numbered applications
- **Comprehensive docstrings** and examples
- **Modern packaging** with pyproject.toml

## 🚦 Common Issues and Solutions

### API Key Issues
- Ensure `ANTHROPIC_API_KEY` is set in your environment
- Check that your API key has sufficient credits
- Verify the key is valid and not expired

### Tool Execution Errors
- Use `--verbose` flag to see detailed error logs
- Check file permissions for file operations
- Verify paths are relative to the working directory
- Ensure bash is available for shell commands

### Python Environment Issues
- Use Python 3.9+ for best compatibility
- Install all dependencies with `pip install -r requirements.txt`
- Consider using a virtual environment to avoid conflicts


## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this educational resource!