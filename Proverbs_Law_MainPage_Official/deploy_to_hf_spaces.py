#!/usr/bin/env python3
"""
Deploy ProVerBs App with Logos to Hugging Face Spaces
"""
import os
import subprocess
import sys
from pathlib import Path

def check_requirements():
    """Check if required tools are installed"""
    print("🔍 Checking requirements...")
    
    # Check Git
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        print("✅ Git installed")
    except:
        print("❌ Git not found. Please install Git first.")
        return False
    
    # Check Hugging Face CLI
    try:
        result = subprocess.run(["pip", "show", "huggingface_hub"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Hugging Face Hub installed")
        else:
            print("⚠️  Installing huggingface_hub...")
            subprocess.run([sys.executable, "-m", "pip", "install", "huggingface_hub"], 
                         check=True)
            print("✅ Hugging Face Hub installed")
    except:
        print("❌ Failed to install huggingface_hub")
        return False
    
    return True

def check_logo_files():
    """Verify all logo files are present"""
    print("\n📁 Checking logo files...")
    
    logo_files = [
        "assets/logo_1.jpg",
        "assets/logo_2.jpg",
        "assets/logo_3.jpg",
    ]
    
    all_present = True
    for logo in logo_files:
        if Path(logo).exists():
            size = Path(logo).stat().st_size / 1024
            print(f"  ✅ {logo} ({size:.2f} KB)")
        else:
            print(f"  ❌ {logo} - MISSING!")
            all_present = False
    
    return all_present

def prepare_deployment():
    """Prepare files for deployment"""
    print("\n📦 Preparing deployment files...")
    
    # Check if README_HF.md should be copied to README.md
    if Path("README_HF.md").exists():
        import shutil
        print("  📝 Copying README_HF.md to README.md...")
        shutil.copy("README_HF.md", "README.md")
        print("  ✅ README.md ready")
    
    # Check critical files
    critical_files = ["app.py", "requirements.txt"]
    for file in critical_files:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MISSING!")
            return False
    
    return True

def create_space_commands(space_name=None):
    """Generate commands for creating and pushing to HF Space"""
    print("\n" + "="*50)
    print("🚀 DEPLOYMENT COMMANDS")
    print("="*50)
    
    if not space_name:
        space_name = input("📝 Enter your Hugging Face Space name (e.g., username/space-name): ").strip()
    
    if not space_name or "/" not in space_name:
        print("❌ Invalid space name format. Use: username/space-name")
        return
    
    print(f"\n✨ Space: {space_name}\n")
    
    print("Run these commands in order:\n")
    print("1️⃣  Initialize Git (if not already done):")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial commit with logos'\n")
    
    print("2️⃣  Login to Hugging Face:")
    print("   python -m huggingface_hub.commands.huggingface_cli login\n")
    
    print("3️⃣  Create and push to Space:")
    print(f"   git remote add space https://huggingface.co/spaces/{space_name}")
    print("   git push --force space main\n")
    
    print("OR use Hugging Face Hub Python API:\n")
    print("---Python Method---")
    print(f"""
from huggingface_hub import HfApi, create_repo

# Login first with your token
api = HfApi()

# Create space
create_repo(
    repo_id="{space_name}",
    repo_type="space",
    space_sdk="gradio"
)

# Upload files
api.upload_folder(
    folder_path=".",
    repo_id="{space_name}",
    repo_type="space",
    ignore_patterns=[".git", "__pycache__", "*.pyc", "tmp_*", "test_*"]
)
""")
    
    print("\n" + "="*50)
    print("📖 After deployment, your Space will be available at:")
    print(f"   https://huggingface.co/spaces/{space_name}")
    print("="*50)

def main():
    """Main deployment preparation"""
    print("="*50)
    print("  ProVerBs Deployment to Hugging Face Spaces")
    print("="*50)
    
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements check failed!")
        return
    
    # Check logos
    if not check_logo_files():
        print("\n⚠️  Warning: Some logo files are missing!")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Prepare files
    if not prepare_deployment():
        print("\n❌ Deployment preparation failed!")
        return
    
    print("\n✅ All checks passed! Ready to deploy.")
    
    # Generate deployment commands
    create_space_commands()
    
    print("\n💡 TIP: Make sure you have a Hugging Face account and token!")
    print("   Get your token at: https://huggingface.co/settings/tokens")

if __name__ == "__main__":
    main()

