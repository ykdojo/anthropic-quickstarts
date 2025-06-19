#!/usr/bin/env python3
"""Example showing Claude-initiated computer use with full agent loop"""

import asyncio
import os
from anthropic import Anthropic
from anthropic.types.beta import BetaToolUseBlock
from computer_use_demo.tools.computer import ComputerTool20250124
from computer_use_demo.tools.collection import ToolCollection

async def main():
    # Initialize the API client
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # Initialize tools
    computer_tool = ComputerTool20250124()
    tool_collection = ToolCollection(computer_tool)
    
    # Initial message asking Claude to take a screenshot
    messages = [{
        "role": "user",
        "content": "Please take a screenshot of the desktop and tell me what you see."
    }]
    
    print("User: Please take a screenshot of the desktop and tell me what you see.")
    print("\n" + "="*50 + "\n")
    
    # Send message to Claude with tool definitions
    response = client.beta.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=messages,
        tools=tool_collection.to_params(),
        betas=["computer-use-2025-01-24"]
    )
    
    # Process Claude's response
    tool_results = []
    for content in response.content:
        if isinstance(content, BetaToolUseBlock):
            print(f"Claude wants to use tool: {content.name}")
            print(f"With parameters: {content.input}")
            
            # Execute the tool that Claude requested
            if content.name == "computer":
                result = await computer_tool(**content.input)
                
                # Format the tool result for the API
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
                
                tool_results.append({
                    "tool_use_id": content.id,
                    "type": "tool_result",
                    "content": tool_result_content
                })
                print(f"Tool executed successfully\n")
        else:
            print(f"Claude: {content.text}")
    
    # If Claude used tools, send the results back
    if tool_results:
        messages.append({
            "role": "assistant",
            "content": response.content
        })
        messages.append({
            "role": "user", 
            "content": tool_results
        })
        
        print("\n" + "="*50 + "\n")
        print("Sending tool results back to Claude...\n")
        
        # Get Claude's final response after seeing the tool results
        final_response = client.beta.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=messages,
            tools=tool_collection.to_params(),
            betas=["computer-use-2025-01-24"]
        )
        
        print("Claude's analysis:")
        for content in final_response.content:
            if hasattr(content, 'text'):
                print(content.text)

if __name__ == "__main__":
    asyncio.run(main())