# NCSU Research Assistant - Web Interface Launcher (PowerShell)
# ==============================================================

Write-Host ""
Write-Host "============================================" -ForegroundColor Red
Write-Host "  NCSU Research Assistant - Web Interface" -ForegroundColor Red
Write-Host "============================================" -ForegroundColor Red
Write-Host ""
Write-Host "Starting Streamlit server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "The web interface will open in your browser." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server." -ForegroundColor Yellow
Write-Host ""

# Set UTF-8 encoding
$env:PYTHONIOENCODING = "utf-8"

# Run Streamlit
streamlit run user_interface.py
