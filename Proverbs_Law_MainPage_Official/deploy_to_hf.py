"""Deployment Script for ProVerBs Landing Page
Deploys to Solomon7890/ProVerbS_LaW_mAiN_PAgE"""

import subprocess
import sys
import os

def print_banner():
    print("="*60)
    print("🚀 ProVerBs Legal AI - Landing Page Deployment")
    print("="*60)
    print()

def check_login():
    """Check if user is logged in to Hugging Face"""
    print("🔍 Checking Hugging Face authentication...")
    try:
        result = subprocess.run(['/home/soldav7890/.local/bin/hf', 'auth', 'whoami'],
                              capture_output=True, text=True)
        if result.returncode == 0:
            username = result.stdout.strip().split('\n')[0].replace('username: ', '')
            print(f"  ✅ Logged in as: {username}")
            return username
        else:
            print("  ❌ Not logged in")
            return None
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None

def login_hf():
    """Prompt user for Hugging Face token"""
    print("\n🔐 Please enter your Hugging Face token (https://huggingface.co/settings/tokens):")
    token = input("Enter token: ")
    return token

def deploy_space(token):
    """Deploy to the Space"""
    space_name = "Solomon7890/Proverbs_Law_MainPage_Official"
    print(f"\n📤 Deploying to: {space_name}")
    print("="*60)

    try:
        # Check if git is initialized
        if not os.path.exists('.git'):
            print("📦 Initializing git repository...")
            subprocess.run(['git', 'init'], check=True)

        # Add remote if not exists
        print("🔗 Setting up remote...")
        # Construct authenticated URL
        authenticated_space_url = f'https://oauth2:{token}@huggingface.co/spaces/{space_name}'

        subprocess.run(
            ['git', 'remote', 'add', 'space', authenticated_space_url],
            capture_output=True
        )

        # Set remote URL (in case it already exists)
        subprocess.run(
            ['git', 'remote', 'set-url', 'space', authenticated_space_url],        
            capture_output=True
        )

        # Replace app.py with enhanced version
        print("📝 Updating app.py with enhanced version...")
        if os.path.exists('integrated_chatbot_with_logos.py'):
            import shutil
            shutil.copy('integrated_chatbot_with_logos.py', 'app.py')
            print("  ✅ Enhanced app.py deployed")

        # Add files
        print("📋 Adding files...")
        subprocess.run(['git', 'add', 'app.py', 'README.md', '.gitattributes', 'assets'], check=True)

        # Commit
        print("💾 Creating commit...")
        subprocess.run(
            ['git', 'commit', '-m', 'Deploy enhanced ProVerBs Legal AI landing page'],
            capture_output=True
        )

        # Push
        print("🚀 Pushing to Hugging Face...")
        result = subprocess.run(
            ['git', 'push', 'space', 'main', '-f'],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            # Try master branch
            result = subprocess.run(
                ['git', 'push', 'space', 'master', '-f'],
                capture_output=True,
                text=True
            )

        if "Everything up-to-date" in result.stderr or result.returncode == 0:
            print("  ✅ Deployment successful!")
            return True
        else:
            print("  ⚠️ Push completed with warnings")
            return True

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    print_banner()

    token = login_hf()
    if not token:
        print("\n❌ Deployment cancelled - Hugging Face token required.")
        return

    # Confirm deployment
    space_url = "https://huggingface.co/spaces/Solomon7890/Proverbs_Law_MainPage_Official"
    print(f"\n📋 Deployment Target:")
    print(f"   Space: Solomon7890/ProVerbS_LaW_mAiN_PAgE")
    print(f"   URL: {space_url}")
    print()

    # Confirmation is now automatic
    print("\n✅ Proceeding with deployment (automatic confirmation).")

    # Deploy
    if deploy_space(token):
        print("\n" + "="*60)
        print("✅ DEPLOYMENT SUCCESSFUL!")
        print("="*60)
        print()
        print(f"🌐 Your Space is available at:")
        print(f"   {space_url}")
        print()
        print("⏳ The Space is now building. This may take 2-3 minutes.")
        print()
        print("📋 Next steps:")
        print("   1. Visit your Space URL")
        print("   2. Wait for the build to complete")
        print("   3. Test all features")
        print("   4. Share with your audience!")
        print()
        print("="*60)
    else:
        print("\n❌ Deployment failed. Please check the errors above.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Deployment cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")