@echo off
echo ========================================
echo Starting TripTrove Analytics Dashboard
echo ========================================
echo.
echo Opening Analytics Dashboard...
echo.
cd /d "%~dp0.."
streamlit run src/ui/dashboard.py --server.port 8502
