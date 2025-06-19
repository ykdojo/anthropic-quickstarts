# Programmatic Computer Use Example

This example demonstrates how to programmatically use the computer-use demo without the Streamlit UI.

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
   podman cp minimal_example.py <container_name>:/home/computeruse/
   ```

3. Run the script inside the container:
   ```bash
   podman exec -it <container_name> python /home/computeruse/minimal_example.py
   ```

## What it does

The script:
1. Initializes the computer tool
2. Takes a screenshot of the virtual desktop
3. Sends the screenshot to Claude asking what it sees
4. Prints Claude's response

## Extending the example

You can extend this to:
- Perform mouse clicks: `await computer_tool(action="left_click", coordinate=[x, y])`
- Type text: `await computer_tool(action="type", text="Hello world")`
- Move mouse: `await computer_tool(action="mouse_move", coordinate=[x, y])`
- Take more screenshots and create an interaction loop