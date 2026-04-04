"""
Deploy ProVerBs Legal AI to HuggingFace Space: Solomon7890/Proverbs_Law777
"""

import os
import shutil
import sys
import tempfile
from pathlib import Path

try:
    from huggingface_hub import HfApi, create_repo
except ImportError:
    print("huggingface_hub not installed. Run: pip install huggingface_hub")
    sys.exit(1)


SPACE_ID = "Solomon7890/Proverbs_Law777"
SPACE_SDK = "docker"
SPACE_HARDWARE = "cpu-basic"

DEPLOY_FILES = [
    "app.py",
    "unified_brain.py",
    "performance_optimizer.py",
    "analytics_seo.py",
    "hf_auth_module.py",
    "agent_orchestrator.py",
    "document_processor.py",
    "case_management_module.py",
    "database_manager.py",
    "handwritten_note_interpreter.py",
    "legal_document_generator.py",
    "supertonic_voice_module.py",
    "requirements.txt",
    "Dockerfile",
]

DEPLOY_DIRS = [
    "assets",
    "utils",
]

EXCLUDE_PATTERNS = [
    ".env", ".env.local", "__pycache__", "*.pyc", "*.db", "*.sqlite",
    "flagged", "node_modules", "frontend", "docker-compose.yml", ".env.template",
]


def main():
    print("Deploying to HuggingFace Space: " + SPACE_ID)
    print("=" * 60)

    api = HfApi()

    # Step 1: Create or verify Space exists
    print("Step 1: Creating/verifying Space...")
    try:
        create_repo(
            repo_id=SPACE_ID,
            repo_type="space",
            space_sdk=SPACE_SDK,
            space_hardware=SPACE_HARDWARE,
            exist_ok=True,
        )
        print("  Space ready: " + SPACE_ID)
    except Exception as e:
        print("  Could not create space: " + str(e))
        print("  Continuing with upload anyway...")

    # Step 2: Prepare staging directory (use temp to avoid OneDrive issues)
    print("Step 2: Preparing files for upload...")
    script_dir = Path(__file__).parent.resolve()
    staging_dir = Path(tempfile.mkdtemp(prefix="hf_staging_"))

    copied_count = 0
    for fname in DEPLOY_FILES:
        src = script_dir / fname
        if src.exists():
            shutil.copy2(src, staging_dir / fname)
            print("  OK: " + fname)
            copied_count += 1
        else:
            print("  MISSING: " + fname)

    for dname in DEPLOY_DIRS:
        src = script_dir / dname
        if src.exists() and src.is_dir():
            shutil.copytree(src, staging_dir / dname,
                            ignore=shutil.ignore_patterns(*EXCLUDE_PATTERNS))
            print("  OK: " + dname + "/")
            copied_count += 1
        else:
            print("  MISSING dir: " + dname + "/")

    print("  Total items staged: " + str(copied_count))

    # Step 3: Upload to Space
    print("Step 3: Uploading to " + SPACE_ID + "...")
    try:
        api.upload_folder(
            folder_path=str(staging_dir),
            repo_id=SPACE_ID,
            repo_type="space",
            commit_message="Deploy ProVerBs Legal AI with HF Auth login tab",
        )
        print("  Upload complete!")
        print("Your Space is live at: https://huggingface.co/spaces/" + SPACE_ID)
    except Exception as e:
        print("  Upload failed: " + str(e))
        sys.exit(1)
    finally:
        if staging_dir.exists():
            shutil.rmtree(staging_dir)
            print("Cleaned up staging directory")

    print("=" * 60)
    print("Deployment complete!")
    print("Space URL: https://huggingface.co/spaces/" + SPACE_ID)


if __name__ == "__main__":
    main()
