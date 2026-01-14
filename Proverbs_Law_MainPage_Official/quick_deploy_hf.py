#!/usr/bin/env python3
"""
Quick Deploy to Hugging Face Spaces - Interactive Version
"""
import os
import sys
from pathlib import Path
import subprocess

def install_hf_hub():
    """Install huggingface_hub if needed"""
    try:
        import huggingface_hub
        print("✅ huggingface_hub already installed")
        return True
    except ImportError:
        print("📦 Installing huggingface_hub...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "huggingface_hub"], 
                         check=True, capture_output=True)
            print("✅ huggingface_hub installed successfully")
            return True
        except:
            print("❌ Failed to install huggingface_hub")
            return False

def main():
    print("="*60)
    print("  🚀 ProVerBs Quick Deploy to Hugging Face Spaces")
    print("="*60)
    print()
    
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    # Check logos
    print("📁 Checking logo files...")
    logos = ["assets/logo_1.jpg", "assets/logo_2.jpg", "assets/logo_3.jpg"]
    logos_ok = all(Path(logo).exists() for logo in logos)
    
    if logos_ok:
        print("✅ All logo files present")
    else:
        print("⚠️  Warning: Some logo files missing")
    
    print()
    
    # Install hub if needed
    if not install_hf_hub():
        print("\n❌ Cannot proceed without huggingface_hub")
        return
    
    print()
    print("="*60)
    print("📝 You need the following to deploy:")
    print("="*60)
    print("1. Hugging Face account (https://huggingface.co/join)")
    print("2. Access token (https://huggingface.co/settings/tokens)")
    print("3. Space name (e.g., Solomon7890/proverbs-law-ai)")
    print()
    
    # Get user input
    print("="*60)
    space_name = input("Enter your Space name (username/space-name): ").strip()
    
    if not space_name or "/" not in space_name:
        print("❌ Invalid format. Use: username/space-name")
        return
    
    print()
    token = input("Enter your Hugging Face token (will be hidden): ").strip()
    
    if not token:
        print("❌ Token required")
        return
    
    print()
    print("="*60)
    print(f"🎯 Deploying to: {space_name}")
    print("="*60)
    print()
    
    try:
        from huggingface_hub import HfApi, create_repo
        
        # Initialize API with token
        api = HfApi(token=token)
        
        # Test connection
        print("🔐 Testing authentication...")
        whoami = api.whoami()
        print(f"✅ Logged in as: {whoami['name']}")
        print()
        
        # Create space
        print(f"📦 Creating Space: {space_name}...")
        try:
            create_repo(
                repo_id=space_name,
                repo_type="space",
                space_sdk="gradio",
                token=token,
                exist_ok=True
            )
            print("✅ Space created/verified")
        except Exception as e:
            print(f"⚠️  Space may already exist: {e}")
        
        print()
        
        # Prepare README
        if Path("README_HF.md").exists():
            import shutil
            print("📝 Copying README_HF.md to README.md...")
            shutil.copy("README_HF.md", "README.md")
        
        # Upload files
        print("📤 Uploading files to Space...")
        print("   This may take a few minutes...")
        
        api.upload_folder(
            folder_path=".",
            repo_id=space_name,
            repo_type="space",
            token=token,
            ignore_patterns=[
                ".git/*",
                ".git",
                "__pycache__/*",
                "*.pyc",
                ".env",
                "*.log",
                "tmp_*",
                "test_*",
                ".DS_Store",
                "deploy_to_hf_spaces.py",
                "quick_deploy_hf.py",
                "DEPLOY_TO_HF.bat",
                "TEST_LOGOS.bat",
                "LOGO_STATUS_REPORT.md",
                "PREVIEW_LOGOS.html"
            ]
        )
        
        print()
        print("="*60)
        print("✅ DEPLOYMENT SUCCESSFUL!")
        print("="*60)
        print()
        print(f"🌐 Your Space is available at:")
        print(f"   https://huggingface.co/spaces/{space_name}")
        print()
        print("⏱️  Note: It may take 1-2 minutes for the Space to build and start")
        print("📺 Watch the build logs on the Space page")
        print()
        print("="*60)
        
    except Exception as e:
        print()
        print("="*60)
        print("❌ DEPLOYMENT FAILED")
        print("="*60)
        print(f"Error: {e}")
        print()
        print("💡 Troubleshooting:")
        print("1. Check your token is valid")
        print("2. Verify space name format (username/space-name)")
        print("3. Ensure you have space creation permissions")
        print("4. Check internet connection")
        print()
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Deployment cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\nPress Enter to exit...")
        input()
