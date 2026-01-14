@echo off
REM Quick Deploy Script for ProVerBs Landing Page
REM Deploys to Solomon7890/ProVerbS_LaW_mAiN_PAgE

color 0A
echo.
echo ============================================================
echo    ProVerBs Legal AI - Quick Deploy to Hugging Face
echo ============================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check if logged in to HF
echo [*] Checking Hugging Face authentication...
huggingface-cli whoami >nul 2>&1
if errorlevel 1 (
    echo [!] Not logged in to Hugging Face
    echo.
    echo Please login first:
    echo    1. Get token from: https://huggingface.co/settings/tokens
    echo    2. Run: huggingface-cli login
    echo    3. Run this script again
    echo.
    pause
    exit /b 1
)

echo [OK] Logged in to Hugging Face
echo.

REM Confirm deployment
echo ============================================================
echo   Target Space: Solomon7890/ProVerbS_LaW_mAiN_PAgE
echo   URL: https://huggingface.co/spaces/Solomon7890/ProVerbS_LaW_mAiN_PAgE
echo ============================================================
echo.
set /p confirm="Deploy enhanced landing page now? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo.
    echo [X] Deployment cancelled
    pause
    exit /b 0
)

echo.
echo [*] Starting deployment...
echo.

REM Run deployment script
python deploy_to_hf.py

echo.
echo ============================================================
echo   Deployment Complete!
echo ============================================================
echo.
pause
