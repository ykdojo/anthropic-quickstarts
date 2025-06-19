# Programmatic Computer Use Example

This example demonstrates how to programmatically use the computer-use demo without the Streamlit UI, showing the full agent loop where Claude decides which tools to use.

## Usage

1. Make sure the container is running:
   ```bash
   podman run -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
       -v $HOME/.anthropic:/home/computeruse/.anthropic \
       -p 5900:5900 -p 8501:8501 -p 6080:6080 -p 8080:8080 \
       -it ghcr.io/anthropics/anthropic-quickstarts:computer-use-demo-latest
   ```

2. Copy the script into the container:
   ```bash
   podman cp claude_agent_loop_example.py <container_name>:/home/computeruse/
   ```

3. Run the script inside the container with your instruction:
   ```bash
   podman exec -it <container_name> python /home/computeruse/claude_agent_loop_example.py "Your instruction here"
   ```

## What it does

The script demonstrates the full agent loop with multi-step task completion:
1. Sends a message to Claude with a multi-step task
2. Claude breaks down the task and executes it step by step
3. The script loops, executing each tool Claude requests
4. Continues until Claude completes all steps
5. Claude provides a final response when the task is done

This matches the Streamlit behavior where Claude can complete complex multi-step tasks in a single conversation.

## Example Commands

```bash
# Simple screenshot
podman exec -it <container_name> python /home/computeruse/claude_agent_loop_example.py "Take a screenshot and describe what you see"

# Multi-step file operations
podman exec -it <container_name> python /home/computeruse/claude_agent_loop_example.py "Open a terminal, create a file called test.txt with 'Hello World', then display its contents"

# Calculator operations
podman exec -it <container_name> python /home/computeruse/claude_agent_loop_example.py "Open the calculator and compute 42 * 17"

# Web browsing
podman exec -it <container_name> python /home/computeruse/claude_agent_loop_example.py "Open Firefox, navigate to example.com, and take a screenshot"
```

## Extending the example

You can extend this to:
- Perform mouse clicks: `await computer_tool(action="left_click", coordinate=[x, y])`
- Type text: `await computer_tool(action="type", text="Hello world")`
- Move mouse: `await computer_tool(action="mouse_move", coordinate=[x, y])`
- Take more screenshots and create an interaction loop