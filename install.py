#!/usr/bin/env python3
"""
VulnerSearch AI Installation Script
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("🔧 Installing VulnerSearch AI requirements...")
    
    try:
        # Install from requirements.txt
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        
        print("✅ All requirements installed successfully!")
        
        # Create necessary directories
        directories = ["logs", "scan_results", "downloaded_tools", "tools"]
        for directory in directories:
            Path(directory).mkdir(exist_ok=True)
            print(f"📁 Created directory: {directory}")
        
        print("\n🚀 VulnerSearch AI is ready to use!")
        print("Run: python main.py")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        print("Try running: pip install --upgrade pip")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_requirements()