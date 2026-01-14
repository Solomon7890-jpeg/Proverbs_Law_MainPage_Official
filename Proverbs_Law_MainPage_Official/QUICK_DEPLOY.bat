@echo off
echo ========================================
echo   ProVerBs - QUICK DEPLOY to HF Spaces
echo ========================================
echo.
echo This script will:
echo  1. Check logo files
echo  2. Install huggingface_hub if needed
echo  3. Deploy your app to HF Spaces
echo.
echo You will need:
echo  - Hugging Face account
echo  - Access token
echo  - Space name (username/space-name)
echo.
pause

cd /d "%~dp0"

python quick_deploy_hf.py

pause
