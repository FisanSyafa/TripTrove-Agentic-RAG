@echo off
echo ========================================
echo TripTrove RAG Setup Script
echo ========================================
echo.

echo [1/4] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.8+
    pause
    exit /b 1
)
echo.

echo [2/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo [3/4] Checking Ollama...
ollama list
if errorlevel 1 (
    echo ERROR: Ollama not found! Please install Ollama first
    pause
    exit /b 1
)
echo.

echo [4/4] Loading data to ChromaDB...
cd /d "%~dp0.."
python src/data_loader.py
if errorlevel 1 (
    echo ERROR: Failed to load data
    pause
    exit /b 1
)
echo.

echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To run the application:
echo   streamlit run app.py
echo.
echo To test in terminal:
echo   python test_agent.py
echo.
pause
