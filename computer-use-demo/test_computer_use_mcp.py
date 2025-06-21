#!/usr/bin/env python3
"""Test script for the Computer Use MCP Server"""

import asyncio
import sys
import os

# Add the current directory to Python path to import the server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from computer_use_mcp_server import computer_use, get_computer_use_info

async def test_server():
    """Test the computer use MCP server functions"""
    
    print("Testing Computer Use MCP Server")
    print("=" * 50)
    
    # Test 1: Get server info
    print("\nTest 1: Getting server information...")
    try:
        info = get_computer_use_info()
        print("Server info:", info)
        print("✓ Server info retrieved successfully")
    except Exception as e:
        print(f"✗ Error getting server info: {e}")
    
    # Test 2: Simple screenshot task
    print("\n\nTest 2: Taking a screenshot...")
    try:
        result = await computer_use(
            instruction="Take a screenshot and briefly describe what you see",
            max_steps=5,
            verbose=True
        )
        print(f"Success: {result['success']}")
        print(f"Steps taken: {result['steps']}")
        print(f"Final response: {result['final_response'][:200]}..." if result.get('final_response') else "No response")
        if result['success']:
            print("✓ Screenshot task completed successfully")
        else:
            print(f"✗ Task failed: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"✗ Error during screenshot task: {e}")
    
    print("\n" + "=" * 50)
    print("Testing complete!")

if __name__ == "__main__":
    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)
    
    # Run the tests
    asyncio.run(test_server())