@echo off
echo ========================================
echo ProVerBs Ultimate Brain - Local Dev Setup
echo ========================================
echo.

cd /d "%~dp0"

echo This will set up local development environment.
echo.
echo Benefits:
echo   - Test features locally before deploying
echo   - Users unaffected by your testing
echo   - Fast iteration cycle
echo   - No internet required for testing
echo.

pause

echo.
echo [1/4] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python first.
    pause
    exit /b 1
)

echo.
echo [2/4] Installing dependencies...
pip install -r requirements.txt

echo.
echo [3/4] Creating .env file for local testing...
if not exist .env (
    echo # Local Development Environment > .env
    echo. >> .env
    echo # Optional API Keys for Testing >> .env
    echo #OPENAI_API_KEY=your_key_here >> .env
    echo #GOOGLE_API_KEY=your_key_here >> .env
    echo #PERPLEXITY_API_KEY=your_key_here >> .env
    echo #NINJAAI_API_KEY=your_key_here >> .env
    echo. >> .env
    echo # Local Development Mode >> .env
    echo DEV_MODE=true >> .env
    
    echo ✅ Created .env file
) else (
    echo ℹ️ .env file already exists
)

echo.
echo [4/4] Creating run script...
echo @echo off > run_local_dev.bat
echo echo Starting ProVerBs Ultimate Brain - Local Development >> run_local_dev.bat
echo echo. >> run_local_dev.bat
echo echo 🌐 App will open at: http://localhost:7860 >> run_local_dev.bat
echo echo 📝 Press Ctrl+C to stop >> run_local_dev.bat
echo echo. >> run_local_dev.bat
echo python app_ultimate_brain.py >> run_local_dev.bat

echo.
echo ========================================
echo ✅ Local Development Setup Complete!
echo ========================================
echo.
echo To start local development:
echo   1. Run: run_local_dev.bat
echo   2. Open: http://localhost:7860
echo   3. Test your features
echo   4. When ready, deploy to production
echo.
echo Production space (unaffected):
echo   https://huggingface.co/spaces/Solomon7890/ProVerbS_LaW_mAiN_PAgE
echo.
echo Press any key to start local dev server now...
pause

echo.
echo Starting local development server...
python app_ultimate_brain.py
