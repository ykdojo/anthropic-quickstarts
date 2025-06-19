#!/usr/bin/env python3
"""Example showing Claude agent that completes multi-step tasks"""

import asyncio
import os
from anthropic import Anthropic
from anthropic.types.beta import BetaToolUseBlock
from computer_use_demo.tools.computer import ComputerTool20250124
from computer_use_demo.tools.bash import BashTool20250124
from computer_use_demo.tools.edit import EditTool20250124
from computer_use_demo.tools.collection import ToolCollection

async def main():
    # Initialize the API client
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # Initialize tools
    computer_tool = ComputerTool20250124()
    bash_tool = BashTool20250124()
    edit_tool = EditTool20250124()
    tool_collection = ToolCollection(computer_tool, bash_tool, edit_tool)
    
    # Initial message with multi-step task
    messages = [{
        "role": "user",
        "content": "Please take a screenshot, then click on the Firefox icon in the taskbar to open it, and take another screenshot to show me Firefox is open."
    }]
    
    print("User:", messages[0]["content"])
    print("\n" + "="*50 + "\n")
    
    # Keep looping until Claude stops using tools
    step = 0
    while True:
        step += 1
        print(f"\n--- Step {step} ---")
        
        # Send message to Claude
        response = client.beta.messages.create(
            model="claude-sonnet-4-20250514",
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
        
        # Process Claude's response and execute any tool requests
        tool_results = []
        has_text_response = False
        
        for content in response.content:
            if isinstance(content, BetaToolUseBlock):
                print(f"Claude wants to use tool: {content.name}")
                print(f"With parameters: {content.input}")
                
                # Execute the requested tool
                if content.name == "computer":
                    result = await computer_tool(**content.input)
                elif content.name == "bash":
                    result = await bash_tool(**content.input)
                elif content.name == "str_replace_based_edit_tool":
                    result = await edit_tool(**content.input)
                else:
                    print(f"Unknown tool: {content.name}")
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
                print(f"Tool executed\n")
            else:
                # Claude provided text response
                print(f"Claude: {content.text}")
                has_text_response = True
        
        # If Claude used tools, send the results back
        if tool_results:
            messages.append({
                "role": "user",
                "content": tool_results
            })
        else:
            # No tools used, Claude is done
            print("\n" + "="*50)
            print("Task completed!")
            break
    
    return messages

if __name__ == "__main__":
    messages = asyncio.run(main())
    
    # Print final summary
    print(f"\nTotal conversation turns: {len(messages)}")
    print(f"Tool uses: {sum(1 for msg in messages if msg['role'] == 'user' and isinstance(msg.get('content'), list) and any(item.get('type') == 'tool_result' for item in msg['content']))}")