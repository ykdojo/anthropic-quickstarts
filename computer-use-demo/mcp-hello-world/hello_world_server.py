#!/usr/bin/env python3
"""
Hello World MCP Server

A simple MCP server that demonstrates basic functionality with:
- A hello world tool
- A greeting resource
- A simple prompt
"""

from mcp.server.fastmcp import FastMCP
from typing import Optional

# Create an MCP server instance
mcp = FastMCP("Hello World MCP")

# Define a simple tool that says hello
@mcp.tool()
def say_hello(name: Optional[str] = None) -> str:
    """
    Say hello to someone
    
    Args:
        name: The name to greet (optional)
    
    Returns:
        A greeting message
    """
    if name:
        return f"Hello, {name}! Welcome to MCP!"
    return "Hello, World! Welcome to MCP!"

# Define a tool that performs a calculation
@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """
    Add two numbers together
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        The sum of a and b
    """
    return a + b

# Define a resource that provides information
@mcp.resource("greeting://{language}")
def get_greeting(language: str) -> str:
    """
    Get a greeting in different languages
    
    Args:
        language: The language code (en, es, fr, de, ja)
    
    Returns:
        A greeting in the specified language
    """
    greetings = {
        "en": "Hello, World!",
        "es": "¡Hola, Mundo!",
        "fr": "Bonjour, le Monde!",
        "de": "Hallo, Welt!",
        "ja": "こんにちは、世界！",
    }
    return greetings.get(language, f"Hello, World! (Unknown language: {language})")

# Define a prompt template
@mcp.prompt()
def greeting_prompt(name: str, language: str = "en") -> str:
    """
    Generate a personalized greeting prompt
    
    Args:
        name: The person's name
        language: The language to use
    
    Returns:
        A prompt for generating a personalized greeting
    """
    return f"Please write a warm, personalized greeting for {name} in {language}. Make it friendly and welcoming."

# Add some metadata about the server
@mcp.tool()
def get_server_info() -> dict:
    """
    Get information about this MCP server
    
    Returns:
        Server metadata
    """
    return {
        "name": "Hello World MCP Server",
        "version": "1.0.0",
        "description": "A simple demonstration of MCP capabilities",
        "tools": ["say_hello", "add_numbers", "get_server_info"],
        "resources": ["greeting://{language}"],
        "prompts": ["greeting_prompt"]
    }

if __name__ == "__main__":
    # This allows the server to run
    import sys
    mcp.run(sys.argv[1:])