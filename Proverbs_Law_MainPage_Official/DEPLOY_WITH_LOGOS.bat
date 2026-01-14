@echo off
REM Deploy AI Legal Chatbot with Rotating Logos
color 0A

echo.
echo ============================================================
echo    Deploy ProVerBs with Rotating Logos
echo ============================================================
echo.

echo [*] Your deployment includes:
echo     - 7 Specialized AI Modes
echo     - 3 Rotating Logos (60 sec rotation)
echo     - Professional Header Design
echo     - Complete Landing Page
echo.

REM Check for assets folder
if not exist "assets\" (
    echo [ERROR] Assets folder not found!
    echo Please ensure assets folder with logos exists.
    pause
    exit /b 1
)

echo [OK] Assets folder found with logos
echo.

REM Check for logo files
set "missing=0"
if not exist "assets\logo_1.jpg" (
    echo [!] logo_1.jpg missing
    set "missing=1"
)
if not exist "assets\logo_2.jpg" (
    echo [!] logo_2.jpg missing
    set "missing=1"
)
if not exist "assets\logo_3.jpg" (
    echo [!] logo_3.jpg missing
    set "missing=1"
)

if "%missing%"=="1" (
    echo [ERROR] Some logo files are missing!
    pause
    exit /b 1
)

echo [OK] All 3 rotating logos found
echo.

REM set /p confirm="Deploy with rotating logos? (Y/N): "
REM if /i not "%confirm%"=="Y" (
REM    echo.
REM    echo [X] Deployment cancelled
REM    pause
REM    exit /b 0
REM )

echo.
echo [*] Backing up current app.py...
if exist app.py (
    copy app.py app_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%.py >nul
    echo [OK] Backup created
)

echo.
echo [*] Deploying version with rotating logos...
copy integrated_chatbot_with_logos.py app.py >nul
echo [OK] App file ready

echo.
echo [*] Starting deployment to Hugging Face...
echo [*] This will upload app.py AND assets folder
echo.

python deploy_to_hf.py

echo.
echo ============================================================
echo   Deployment Complete!
echo ============================================================
echo.
echo Your Space with rotating logos is now live!
echo Visit: https://huggingface.co/spaces/Solomon7890/ProVerbS_LaW_mAiN_PAgE
echo.
echo NOTE: Wait 60 seconds to see the logos rotate!
echo.
pause
