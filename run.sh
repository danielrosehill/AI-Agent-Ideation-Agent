#!/bin/bash

# AI Agent Ideation Generator Run Script
# This script activates the virtual environment and runs the GUI application

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found."
    echo "Please run setup.sh first to create the virtual environment and install dependencies."
    echo "  ./setup.sh"
    exit 1
fi

# Activate virtual environment and run the application
echo "Starting AI Agent Ideation Generator GUI..."
source venv/bin/activate
python3 gui_generate_agent_ideas.py

# Deactivate virtual environment on exit
deactivate
