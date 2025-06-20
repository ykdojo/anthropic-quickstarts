#!/bin/bash

# Simple clipboard sharing via file

CLIPBOARD_FILE="/home/computeruse/clipboard.txt"

case "$1" in
    "send")
        # Send Mac clipboard to container as a file
        pbpaste | podman exec -i computer-use-vscode tee "$CLIPBOARD_FILE" > /dev/null
        echo "Clipboard saved to container at: $CLIPBOARD_FILE"
        echo "Content:"
        pbpaste
        ;;
    "get")
        # Get clipboard file from container to Mac clipboard
        podman exec computer-use-vscode cat "$CLIPBOARD_FILE" 2>/dev/null | pbcopy
        echo "Container clipboard loaded to Mac clipboard"
        ;;
    "show")
        # Show what's in the container clipboard file
        echo "Container clipboard file contents:"
        podman exec computer-use-vscode cat "$CLIPBOARD_FILE" 2>/dev/null || echo "(empty or not found)"
        ;;
    *)
        echo "Usage: $0 {send|get|show}"
        echo "  send - Copy Mac clipboard to container file"
        echo "  get  - Copy container file to Mac clipboard"
        echo "  show - Display container clipboard file"
        ;;
esac