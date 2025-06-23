#!/bin/bash

set -e

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export DISPLAY=:${DISPLAY_NUM}
"$SCRIPT_DIR/xvfb_startup.sh"
"$SCRIPT_DIR/tint2_startup.sh"
"$SCRIPT_DIR/mutter_startup.sh"
"$SCRIPT_DIR/x11vnc_startup.sh"
