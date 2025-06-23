#!/bin/bash
set -e

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run scripts from their absolute paths
"$SCRIPT_DIR/start_all.sh"
"$SCRIPT_DIR/novnc_startup.sh"

# Run python scripts from home directory
cd /home/computeruse
python "$SCRIPT_DIR/http_server.py" > /tmp/server_logs.txt 2>&1 &

STREAMLIT_SERVER_PORT=8501 python -m streamlit run computer_use_demo/streamlit.py > /tmp/streamlit_stdout.log &

echo "✨ Computer Use Demo is ready!"
echo "➡️  Open http://localhost:8080 in your browser to begin"

# Keep the container running
tail -f /dev/null
