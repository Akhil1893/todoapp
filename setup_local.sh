#!/bin/bash

echo "🚀 UPI Expense Tracker - Local Setup"
echo "===================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To run the application:"
echo "1. Open terminal/command prompt"
echo "2. Navigate to this directory"
echo "3. Run: source venv/bin/activate  (Linux/Mac) or venv\\Scripts\\activate (Windows)"
echo "4. Run: python app.py"
echo "5. Open browser to: http://localhost:5000"
echo ""
echo "🎉 Enjoy tracking your UPI expenses!"