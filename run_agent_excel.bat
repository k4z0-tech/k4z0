@echo off
echo ========================================
echo Order Analysis Agent - Excel Feedback Mode
echo ========================================
echo.
echo This agent creates an Excel file for you to fill in feedback.
echo.
echo How it works:
echo   1. Agent analyzes your orders and finds delayed ones
echo   2. Agent creates an Excel file on your desktop
echo   3. You fill in the feedback in the Excel file
echo   4. You run the agent again to process the feedback
echo   5. Agent learns from your feedback
echo.
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

REM Run the Excel-based agent
echo Starting Excel-based Order Analysis Agent...
echo.
.venv\Scripts\python.exe src\order_agent_excel.py

echo.
echo ========================================
echo Agent Finished
echo ========================================
pause
