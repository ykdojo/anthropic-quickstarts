# Programmatic Computer Use Example

This example demonstrates how to programmatically use the computer-use demo without the Streamlit UI, showing the full agent loop where Claude decides which tools to use.

## Enhanced Container with VS Code

The container now includes:
- **VS Code** pre-installed with the desktop environment
- **Sourcegraph Amp extension** (an agentic coding tool) pre-installed
- **claude_agent_loop_example.py** automatically included in the build

## Usage

### Building the Enhanced Container (Optional)

To build the container with VS Code and Amp extension:
```bash
podman build . -t computer-use-demo-vscode:local
```

### Running the Container

1. Run the container:
   ```bash
   podman run -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
       -v $(pwd)/computer_use_demo:/home/computeruse/computer_use_demo/ \
       -v $HOME/.anthropic:/home/computeruse/.anthropic \
       -p 5900:5900 -p 8501:8501 -p 6080:6080 -p 8080:8080 \
       --name computer-use-vscode \
       -it computer-use-demo-vscode:local
   ```

2. Run the script inside the container with your instruction:
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

# VS Code operations
podman exec -it <container_name> python /home/computeruse/claude_agent_loop_example.py "Open VS Code and create a new Python file with a hello world program"

# Using the Amp extension
podman exec -it <container_name> python /home/computeruse/claude_agent_loop_example.py "Open VS Code and show me the Amp extension by Sourcegraph"
```
