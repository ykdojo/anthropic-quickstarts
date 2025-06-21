# Hello World MCP Server

A simple Model Context Protocol (MCP) server demonstrating basic functionality.

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

## Testing the Server

Once running, you can:
1. Call `say_hello()` or `say_hello("Your Name")`
2. Use `add_numbers(5, 3)` to get 8
3. Access resources like `greeting://es` for Spanish greeting
4. Use the prompt template for personalized greetings