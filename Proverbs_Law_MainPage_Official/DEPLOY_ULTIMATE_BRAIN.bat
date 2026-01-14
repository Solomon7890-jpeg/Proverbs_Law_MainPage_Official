@echo off
echo ========================================
echo ProVerBs Ultimate Legal AI Brain v3.0
echo Deployment Script
echo ========================================
echo.

cd /d "%~dp0"

echo [1/5] Backing up current files...
if exist app.py (
    copy app.py app_backup_v2.py
)

echo [2/5] Copying Ultimate Brain files...
copy unified_brain.py .
copy app_ultimate_brain.py app.py

echo [3/5] Updating requirements...
copy requirements_multi_ai.txt requirements.txt

echo [4/5] Adding files to git...
git add unified_brain.py app.py requirements.txt README_ULTIMATE_BRAIN.md

echo [5/5] Committing and pushing...
git commit -m "🧠 Deploy Ultimate Brain v3.0: 100+ Reasoning Protocols + Multi-AI + Supertonic"
git push origin main

echo.
echo ========================================
echo ✅ DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo 🌐 Your Ultimate Brain Space:
echo https://huggingface.co/spaces/Solomon7890/ProVerbS_LaW_mAiN_PAgE
echo.
echo 🔑 Don't forget to add API keys in Space Settings:
echo    - OPENAI_API_KEY
echo    - GOOGLE_API_KEY  
echo    - PERPLEXITY_API_KEY
echo    - NINJAAI_API_KEY
echo.
echo 🧠 Features:
echo    - 100+ Reasoning Protocols
echo    - 6 AI Models
echo    - 7 Legal Modes
echo    - Supertonic Audio
echo.
echo 💡 Tip: HuggingFace model works without API keys!
echo.
pause
