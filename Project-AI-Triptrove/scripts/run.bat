@echo off
echo ========================================
echo Starting TripTrove AI Assistant
echo ========================================
echo.
echo Opening Streamlit UI...
echo.
cd /d "%~dp0.."
streamlit run src/ui/app.py
