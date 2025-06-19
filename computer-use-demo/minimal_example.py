#!/usr/bin/env python3
"""Minimal example showing direct API usage"""

import asyncio
import os
from anthropic import Anthropic
from computer_use_demo.tools.computer import ComputerTool20250124

async def main():
    # Initialize the API client
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # Initialize the computer tool
    computer_tool = ComputerTool20250124()
    
    # Take a screenshot using the tool directly
    print("Taking screenshot...")
    screenshot_result = await computer_tool(action="screenshot")
    
    if screenshot_result.base64_image:
        print(f"Screenshot taken! Base64 data length: {len(screenshot_result.base64_image)}")
        
        # Now send it to Claude
        response = client.beta.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What do you see in this screenshot?"
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": screenshot_result.base64_image
                        }
                    }
                ]
            }],
            betas=["computer-use-2025-01-24"]
        )
        
        print("\nClaude's response:")
        print(response.content[0].text)
    else:
        print("Failed to take screenshot")

if __name__ == "__main__":
    asyncio.run(main())