#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define the directory for the virtual environment
VENV_DIR="venv"

# Check if a custom virtual environment directory is provided
if [ ! -z "$1" ]; then
    VENV_DIR="$1"
fi

# Check if the virtual environment already exists
if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment already exists in $VENV_DIR"
else
    # Create the virtual environment
    echo "Creating virtual environment in $VENV_DIR"
    python3 -m venv "$VENV_DIR"
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip
pip3 install --upgrade pip

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt"
    pip3 install -r requirements.txt
else
    echo "No requirements.txt found, skipping dependency installation"
fi

echo "Virtual environment setup complete. To activate, run 'source $VENV_DIR/bin/activate'"
