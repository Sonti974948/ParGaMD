#!/usr/bin/env python3
"""
Helper script to prepare and upload files to GitHub
"""

import os
import subprocess
import sys

def check_git_installed():
    """Check if git is installed"""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def initialize_git_repo():
    """Initialize git repository"""
    if not os.path.exists(".git"):
        print("Initializing git repository...")
        subprocess.run(["git", "init"], check=True)
    else:
        print("Git repository already exists.")

def add_files():
    """Add all files to git"""
    print("Adding files to git...")
    subprocess.run(["git", "add", "."], check=True)

def create_initial_commit():
    """Create initial commit"""
    print("Creating initial commit...")
    subprocess.run(["git", "commit", "-m", "Initial commit: ParGaMD Reweighting Tool"], check=True)

def setup_remote_repo():
    """Guide user to set up remote repository"""
    print("\n" + "="*60)
    print("SETUP REMOTE GITHUB REPOSITORY")
    print("="*60)
    print("1. Go to https://github.com/new")
    print("2. Create a new repository named 'pargamd-reweighting'")
    print("3. DO NOT initialize with README, .gitignore, or license (we already have these)")
    print("4. Copy the repository URL")
    print("5. Run the following commands:")
    print()
    print("   git remote add origin https://github.com/YOUR_USERNAME/pargamd-reweighting.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    print()
    print("Replace YOUR_USERNAME with your actual GitHub username!")
    print("="*60)

def main():
    """Main function"""
    print("ParGaMD Reweighting Tool - GitHub Upload Helper")
    print("="*50)
    
    if not check_git_installed():
        print("❌ Git is not installed. Please install git first.")
        print("   Download from: https://git-scm.com/downloads")
        sys.exit(1)
    
    try:
        initialize_git_repo()
        add_files()
        create_initial_commit()
        setup_remote_repo()
        
        print("\n✅ Local git repository is ready!")
        print("📝 Follow the steps above to create your GitHub repository.")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()



