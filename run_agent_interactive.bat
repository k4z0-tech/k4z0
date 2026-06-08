@echo off
echo ========================================
echo Order Analysis Agent - Interactive Mode
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found!
    echo Please run: python -m venv .venv
    pause
    exit /b 1
)

REM Check if data file exists
if not exist "order_train_data.xlsx" (
    echo [ERROR] Data file 'order_train_data.xlsx' not found!
    echo Please ensure the file exists in the project root.
    pause
    exit /b 1
)

REM Run the interactive agent
echo Starting Interactive Order Analysis Agent...
echo.
echo This agent will:
echo   1. Analyze your orders and find delayed ones
echo   2. Show you a summary of delayed orders
echo   3. Ask you to provide feedback for each order
echo   4. Learn from your feedback
echo   5. Generate a report
echo.
echo Press Ctrl+C at any time to exit.
echo.
pause

.venv\Scripts\python.exe src\order_agent_interactive.py

echo.
echo ========================================
echo Analysis Complete
echo ========================================
pause
