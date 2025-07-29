@echo off
echo 🚀 UPI Expense Tracker - Local Setup (Windows)
echo ==========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

echo.
echo ✅ Setup complete!
echo.
echo 🚀 To run the application:
echo 1. Open Command Prompt
echo 2. Navigate to this directory
echo 3. Run: venv\Scripts\activate
echo 4. Run: python app.py
echo 5. Open browser to: http://localhost:5000
echo.
echo 🎉 Enjoy tracking your UPI expenses!
pause