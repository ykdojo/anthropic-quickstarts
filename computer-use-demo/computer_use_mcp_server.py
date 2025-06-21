#!/usr/bin/env python3
"""
Computer Use MCP Server

An MCP server that exposes computer use functionality through a single tool.
This wraps the Claude agent loop to execute multi-step computer use tasks.
"""

import asyncio
import os
from typing import Optional, List, Dict, Any
from mcp.server.fastmcp import FastMCP
from anthropic import Anthropic
from anthropic.types.beta import BetaToolUseBlock
from computer_use_demo.tools.computer import ComputerTool20250124
from computer_use_demo.tools.bash import BashTool20250124
from computer_use_demo.tools.edit import EditTool20250124
from computer_use_demo.tools.collection import ToolCollection

# Create an MCP server instance
mcp = FastMCP("Computer Use MCP")

# Global client (will be initialized once)
_anthropic_client = None

def get_anthropic_client():
    """Get or create the Anthropic client"""
    global _anthropic_client
    if _anthropic_client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        _anthropic_client = Anthropic(api_key=api_key)
    return _anthropic_client

@mcp.tool()
async def computer_use(
    instruction: str,
    max_steps: Optional[int] = 20,
    verbose: Optional[bool] = True
) -> Dict[str, Any]:
    """
    Execute a computer use task with Claude
    
    Args:
        instruction: The task instruction for Claude to execute
        max_steps: Maximum number of steps to allow (default: 20)
        verbose: Whether to include detailed step information (default: True)
    
    Returns:
        A dictionary containing:
        - success: Whether the task completed successfully
        - steps: Number of steps taken
        - final_response: Claude's final response
        - tool_uses: List of tools used during execution
        - error: Error message if something went wrong (optional)
    """
    try:
        # Initialize the API client
        client = get_anthropic_client()
        
        # Initialize tools
        computer_tool = ComputerTool20250124()
        bash_tool = BashTool20250124()
        edit_tool = EditTool20250124()
        tool_collection = ToolCollection(computer_tool, bash_tool, edit_tool)
        
        # Track execution
        tool_uses = []
        messages = [{
            "role": "user",
            "content": instruction
        }]
        
        # Execute the agent loop
        step = 0
        final_response = ""
        
        while step < max_steps:
            step += 1
            
            # Send message to Claude
            response = client.beta.messages.create(
                model="claude-opus-4-20250514",
                max_tokens=4096,
                messages=messages,
                tools=tool_collection.to_params(),
                betas=["computer-use-2025-01-24"]
            )
            
            # Add Claude's response to messages
            messages.append({
                "role": "assistant",
                "content": response.content
            })
            
            # Process Claude's response
            tool_results = []
            has_text_response = False
            
            for content in response.content:
                if isinstance(content, BetaToolUseBlock):
                    # Record tool use
                    tool_uses.append({
                        "step": step,
                        "tool": content.name,
                        "parameters": content.input
                    })
                    
                    # Execute the requested tool
                    if content.name == "computer":
                        result = await computer_tool(**content.input)
                    elif content.name == "bash":
                        result = await bash_tool(**content.input)
                    elif content.name == "str_replace_based_edit_tool":
                        result = await edit_tool(**content.input)
                    else:
                        continue
                    
                    # Format the tool result
                    tool_result_content = []
                    if result.output:
                        tool_result_content.append({
                            "type": "text",
                            "text": result.output
                        })
                    if result.base64_image:
                        tool_result_content.append({
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": result.base64_image
                            }
                        })
                    if result.error:
                        tool_result_content = [{
                            "type": "text", 
                            "text": f"Error: {result.error}"
                        }]
                    
                    tool_results.append({
                        "tool_use_id": content.id,
                        "type": "tool_result",
                        "content": tool_result_content
                    })
                else:
                    # Claude provided text response
                    final_response = content.text
                    has_text_response = True
            
            # If Claude used tools, send the results back
            if tool_results:
                messages.append({
                    "role": "user",
                    "content": tool_results
                })
            else:
                # No tools used, Claude is done
                break
        
        return {
            "success": True,
            "steps": step,
            "final_response": final_response,
            "tool_uses": tool_uses if verbose else len(tool_uses),
            "instruction": instruction
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "instruction": instruction
        }

@mcp.tool()
def get_computer_use_info() -> Dict[str, Any]:
    """
    Get information about the computer use capabilities
    
    Returns:
        Information about available tools and capabilities
    """
    return {
        "description": "Computer Use MCP Server - Execute multi-step computer tasks with Claude",
        "available_tools": [
            {
                "name": "computer",
                "actions": ["screenshot", "left_click", "right_click", "double_click", 
                           "type", "key", "mouse_move", "drag", "scroll"]
            },
            {
                "name": "bash",
                "description": "Execute bash commands"
            },
            {
                "name": "str_replace_based_edit_tool",
                "description": "Edit files with string replacement"
            }
        ],
        "model": "claude-opus-4-20250514",
        "max_steps_default": 20,
        "requires": ["ANTHROPIC_API_KEY environment variable"]
    }

if __name__ == "__main__":
    # This allows the server to run
    import sys
    # Default to stdio transport if not specified
    transport = sys.argv[1] if len(sys.argv) > 1 else "stdio"
    mcp.run(transport=transport)