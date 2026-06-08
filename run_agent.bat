@echo off
echo ========================================
echo Order Analysis Agent
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

REM Run the agent
echo Starting Order Analysis Agent...
echo.
.venv\Scripts\python.exe src\order_agent_simple.py

echo.
echo ========================================
echo Analysis Complete
echo ========================================
pause
