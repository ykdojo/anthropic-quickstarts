#!/bin/bash

echo "Opening all exposed container ports in browser..."

# noVNC web interface (for viewing the desktop)
echo "Opening noVNC interface on port 6080..."
open "http://localhost:6080/vnc.html?autoconnect=true"

# Streamlit interface
echo "Opening Streamlit interface on port 8501..."
open "http://localhost:8501"

# HTTP server
echo "Opening HTTP server on port 8080..."
open "http://localhost:8080"

echo "All browser-accessible ports opened!"
echo ""
echo "Note: Port 5900 is for VNC clients (not browser-accessible)"
echo "Use a VNC client like VNC Viewer to connect to localhost:5900 if needed"