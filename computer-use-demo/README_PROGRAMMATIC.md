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
   podman cp claude_agent_example.py <container_name>:/home/computeruse/
   ```

3. Run the script inside the container:
   ```bash
   podman exec -it <container_name> python /home/computeruse/claude_agent_example.py
   ```

## What it does

The script demonstrates the full agent loop:
1. Sends a message to Claude asking it to take a screenshot
2. Claude responds with a tool use request for the computer tool
3. The script executes the tool that Claude requested
4. Sends the tool results (screenshot) back to Claude
5. Claude analyzes the results and describes what it sees

This shows how Claude makes decisions about which tools to use based on user requests.

## Extending the example

You can extend this to:
- Perform mouse clicks: `await computer_tool(action="left_click", coordinate=[x, y])`
- Type text: `await computer_tool(action="type", text="Hello world")`
- Move mouse: `await computer_tool(action="mouse_move", coordinate=[x, y])`
- Take more screenshots and create an interaction loop