@echo off
REM Local Preview - Test Before Deploying
color 0B

echo.
echo ============================================================
echo    LOCAL PREVIEW - Test Your App Before Deployment
echo ============================================================
echo.

echo [*] This will start a local server so you can preview:
echo     - Your rotating logos (watch them change every 60 sec)
echo     - All 7 AI assistant modes
echo     - Complete landing page design
echo     - All features and tabs
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check for required files
if not exist "integrated_chatbot_with_logos.py" (
    echo [ERROR] integrated_chatbot_with_logos.py not found!
    echo Please ensure you're in the ProVerbS_LaW_mAiN_PAgE folder
    pause
    exit /b 1
)

if not exist "assets\" (
    echo [ERROR] Assets folder not found!
    echo Your logos won't display without the assets folder
    pause
    exit /b 1
)

echo [OK] All files found
echo.

echo ============================================================
echo   Starting Local Preview Server...
echo ============================================================
echo.
echo [*] The app will open in your browser automatically
echo [*] Server URL: http://localhost:7860
echo.
echo [*] IMPORTANT: Watch the logos rotate every 60 seconds!
echo.
echo [!] Press Ctrl+C to stop the server when done previewing
echo.
echo ============================================================
echo.

REM Run the app locally
python integrated_chatbot_with_logos.py

echo.
echo ============================================================
echo   Preview Ended
echo ============================================================
echo.
pause
