#!/bin/bash
echo "========================================"
echo "Order Analysis Agent"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -f ".venv/bin/python" ] && [ ! -f ".venv/Scripts/python.exe" ]; then
    echo "[ERROR] Virtual environment not found!"
    echo "Please run: python -m venv .venv"
    exit 1
fi

# Check if data file exists
if [ ! -f "order_train_data.xlsx" ]; then
    echo "[ERROR] Data file 'order_train_data.xlsx' not found!"
    echo "Please ensure the file exists in the project root."
    exit 1
fi

# Run the agent
echo "Starting Order Analysis Agent..."
echo ""

if [ -f ".venv/Scripts/python.exe" ]; then
    .venv/Scripts/python.exe src/order_agent_simple.py
else
    .venv/bin/python src/order_agent_simple.py
fi

echo ""
echo "========================================"
echo "Analysis Complete"
echo "========================================"
