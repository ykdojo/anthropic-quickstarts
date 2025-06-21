# MCP Servers for Computer Use Demo

This directory contains two MCP servers:
1. **Hello World MCP Server** - A simple example demonstrating basic MCP functionality
2. **Computer Use MCP Server** - Exposes computer use capabilities through MCP

## Features

### Tools
- `say_hello(name?)` - Says hello with an optional name
- `add_numbers(a, b)` - Adds two numbers
- `get_server_info()` - Returns server metadata

### Resources
- `greeting://{language}` - Get greetings in different languages (en, es, fr, de, ja)

### Prompts
- `greeting_prompt(name, language)` - Generate personalized greeting prompts

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or using uv
uv pip install -r requirements.txt
```

## Running the Server

### Test with MCP Inspector
```bash
mcp dev hello_world_server.py
```
This opens an interactive inspector in your browser to test the server.

### Install in Claude Desktop
```bash
mcp install hello_world_server.py
```

### Manual Configuration for Claude Desktop
Add to your Claude Desktop config file (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "hello-world": {
      "command": "python",
      "args": ["/path/to/hello_world_server.py"]
    }
  }
}
```

## Testing the Hello World Server

Once running, you can:
1. Call `say_hello()` or `say_hello("Your Name")`
2. Use `add_numbers(5, 3)` to get 8
3. Access resources like `greeting://es` for Spanish greeting
4. Use the prompt template for personalized greetings

---

## Computer Use MCP Server

The `computer_use_mcp_server.py` provides MCP access to computer use capabilities.

### Features

#### Main Tool
- `computer_use(instruction, max_steps?, verbose?)` - Execute multi-step computer tasks
  - `instruction`: The task to perform (e.g., "Take a screenshot and describe what you see")
  - `max_steps`: Maximum steps allowed (default: 20)
  - `verbose`: Include detailed step information (default: true)

#### Info Tool
- `get_computer_use_info()` - Get information about available capabilities

### Running the Computer Use Server

**Requirements**: 
- Must be run inside the computer-use-demo container
- Requires `ANTHROPIC_API_KEY` environment variable

```bash
# Inside the container
source .venv/bin/activate
mcp dev computer_use_mcp_server.py
```

### Example Usage

```python
# Execute a simple task
computer_use("Take a screenshot and tell me what you see")

# Execute a multi-step task
computer_use("Open VS Code and create a new Python file with hello world")

# Get information about capabilities
get_computer_use_info()
```

### Claude Desktop Configuration

Add to your config file:
```json
{
  "mcpServers": {
    "computer-use": {
      "command": "python",
      "args": ["/path/to/computer_use_mcp_server.py"]
    }
  }
}
```

Note: The server will use the `ANTHROPIC_API_KEY` from your environment variables.