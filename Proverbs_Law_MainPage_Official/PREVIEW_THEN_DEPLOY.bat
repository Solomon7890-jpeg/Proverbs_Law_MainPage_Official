@echo off
REM Complete Workflow: Preview Locally THEN Deploy
color 0A

echo.
echo ============================================================
echo    PREVIEW THEN DEPLOY - Safe Deployment Workflow
echo ============================================================
echo.

echo STEP 1: PREVIEW LOCALLY
echo ============================================================
echo.
echo [*] First, we'll start a local preview so you can test
echo     everything before deploying to Hugging Face.
echo.
set /p preview="Start local preview now? (Y/N): "
if /i not "%preview%"=="Y" (
    echo.
    echo [X] Preview cancelled
    pause
    exit /b 0
)

echo.
echo [*] Starting local preview...
echo [*] The app will open at http://localhost:7860
echo.
echo PREVIEW CHECKLIST:
echo [ ] Check that all 3 logos display
echo [ ] Wait 60+ seconds to see logos rotate
echo [ ] Test all 7 AI assistant modes
echo [ ] Navigate through all tabs
echo [ ] Test on mobile view (resize browser)
echo [ ] Check that everything looks good
echo.
echo [!] Press Ctrl+C when you're done previewing
echo.
pause

REM Run local preview
python integrated_chatbot_with_logos.py

echo.
echo ============================================================
echo.

echo STEP 2: DEPLOY TO HUGGING FACE
echo ============================================================
echo.
echo [*] Did everything look good in the preview?
echo [*] Are you ready to deploy to Hugging Face?
echo.
set /p deploy="Deploy to Hugging Face now? (Y/N): "
if /i not "%deploy%"=="Y" (
    echo.
    echo [X] Deployment cancelled
    echo.
    echo You can run this script again when ready!
    pause
    exit /b 0
)

echo.
echo [*] Great! Proceeding with deployment...
echo.

REM Backup current app.py
if exist app.py (
    echo [*] Backing up current app.py...
    copy app.py app_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%.py >nul
    echo [OK] Backup created
)

echo.
echo [*] Preparing deployment files...
copy integrated_chatbot_with_logos.py app.py >nul
echo [OK] App file ready

echo.
echo [*] Starting deployment to Hugging Face...
echo.

python deploy_to_hf.py

echo.
echo ============================================================
echo   Deployment Complete!
echo ============================================================
echo.
echo Your Space is now live with rotating logos!
echo Visit: https://huggingface.co/spaces/Solomon7890/ProVerbS_LaW_mAiN_PAgE
echo.
echo Remember: Wait 60+ seconds to see the logos rotate on the live site!
echo.
pause
