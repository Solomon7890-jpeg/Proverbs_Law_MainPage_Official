@echo off
echo ========================================
echo ProVerBs - Deploy to Hugging Face Spaces
echo ========================================
echo.

cd /d "%~dp0"

echo Running deployment preparation...
python deploy_to_hf_spaces.py

echo.
echo ========================================
echo Deployment preparation complete!
echo Follow the instructions above to deploy.
echo ========================================
echo.
pause
