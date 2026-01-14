@echo off
REM Deploy Integrated AI Legal Chatbot to Hugging Face
color 0A

echo.
echo ============================================================
echo    Deploy AI Legal Chatbot Integration
echo ============================================================
echo.

echo [*] This will deploy your chatbot with 7 specialized modes:
echo.
echo     1. Navigation Guide
echo     2. General Legal Assistant
echo     3. Document Validator
echo     4. Legal Research
echo     5. Etymology Expert
echo     6. Case Management
echo     7. Regulatory Updates
echo.

set /p confirm="Continue with deployment? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo.
    echo [X] Deployment cancelled
    pause
    exit /b 0
)

echo.
echo [*] Backing up current app.py...
if exist app.py (
    copy app.py app_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%.py >nul
    echo [OK] Backup created
) else (
    echo [!] No existing app.py found
)

echo.
echo [*] Deploying integrated chatbot version...
copy integrated_chatbot_app.py app.py >nul
echo [OK] integrated_chatbot_app.py copied to app.py

echo.
echo [*] Starting deployment to Hugging Face...
python deploy_to_hf.py

echo.
echo ============================================================
echo   Deployment Complete!
echo ============================================================
echo.
echo Your chatbot with 7 specialized modes is now live!
echo Visit: https://huggingface.co/spaces/Solomon7890/ProVerbS_LaW_mAiN_PAgE
echo.
pause
