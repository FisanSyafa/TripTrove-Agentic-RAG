@echo off
echo ========================================
echo Starting TripTrove Advanced UI
echo ========================================
echo.
echo Opening Advanced UI with extra features...
echo.
cd /d "%~dp0.."
streamlit run src/ui/advanced_app.py --server.port 8503
