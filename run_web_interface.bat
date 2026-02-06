@echo off
REM NCSU Research Assistant - Web Interface Launcher
REM ================================================

echo.
echo ============================================
echo   NCSU Research Assistant - Web Interface
echo ============================================
echo.
echo Starting Streamlit server...
echo.
echo The web interface will open in your browser.
echo Press Ctrl+C to stop the server.
echo.

REM Set UTF-8 encoding
chcp 65001 > nul
set PYTHONIOENCODING=utf-8

REM Run Streamlit
streamlit run user_interface.py

pause
