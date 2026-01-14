@echo off
REM Helper Script to Deploy to HF via Web Interface
color 0B

echo.
echo ============================================================
echo    HUGGING FACE DEPLOYMENT HELPER
echo ============================================================
echo.

echo [*] This script will:
echo     1. Copy app.py content to clipboard
echo     2. Open HF Space editor in browser
echo     3. Guide you through manual upload
echo.

pause

echo.
echo [*] Step 1: Copying app.py to clipboard...
echo.

REM Copy app.py content to clipboard
powershell -command "Get-Content app.py -Raw | Set-Clipboard"

echo [OK] app.py content copied to clipboard!
echo.
echo ============================================================
echo    NEXT STEPS:
echo ============================================================
echo.
echo 1. Browser will open HF Space editor
echo 2. Click "Edit this file" (pencil icon)
echo 3. Select All (Ctrl+A) and Delete
echo 4. Paste (Ctrl+V) - your app.py is in clipboard!
echo 5. Scroll down and click "Commit changes to main"
echo 6. Wait 2-3 minutes for rebuild
echo.

pause

echo.
echo [*] Opening HF Space in browser...
echo.

start https://huggingface.co/spaces/Solomon7890/ProVerbS_LaW_mAiN_PAgE/tree/main

echo.
echo ============================================================
echo    INSTRUCTIONS:
echo ============================================================
echo.
echo ON THE WEB PAGE THAT JUST OPENED:
echo.
echo 1. Click "app.py" filename
echo 2. Click "Edit this file" button (pencil icon, top right)
echo 3. In the editor:
echo    - Press Ctrl+A (select all)
echo    - Press Delete
echo    - Press Ctrl+V (paste - your content is ready!)
echo 4. Scroll down
echo 5. Click "Commit changes to main"
echo.
echo DONE! Wait 2-3 minutes, then refresh your Space!
echo.
echo Your Space URL:
echo https://huggingface.co/spaces/Solomon7890/ProVerbS_LaW_mAiN_PAgE
echo.
echo ============================================================
echo.

pause
