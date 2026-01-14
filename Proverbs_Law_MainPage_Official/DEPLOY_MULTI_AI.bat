@echo off
echo ========================================
echo ProVerBs Legal AI - Deploy Multi-AI Version
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] Backing up current app.py...
if exist app.py (
    copy app.py app_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.py
)

echo [2/4] Copying multi-AI version...
copy app_complete_multi_ai.py app.py
copy requirements_multi_ai.txt requirements.txt

echo [3/4] Adding to git...
git add app.py requirements.txt README_MULTI_AI.md

echo [4/4] Committing and pushing...
git commit -m "Deploy Multi-AI version with GPT-4, Gemini, Perplexity, NinjaAI, LM Studio + Supertonic"
git push origin main

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Your Space URL:
echo https://huggingface.co/spaces/Solomon7890/ProVerbS_LaW_mAiN_PAgE
echo.
echo Don't forget to add API keys in Space Settings!
echo.
pause
