"""
Setup script for Arovia - AI Health Desk Agent
"""
import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.11+"""
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ is required. Current version:", sys.version)
        return False
    print(f"✅ Python version: {sys.version}")
    return True


def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        # Install using pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False


def setup_environment():
    """Setup environment variables"""
    print("🔧 Setting up environment...")
    
    env_file = Path("env.example")
    if env_file.exists():
        print("📝 Please copy env.example to .env and add your API keys:")
        print("   cp env.example .env")
        print("   # Edit .env and add your GROQ_API_KEY")
    else:
        print("⚠️  env.example not found")


def test_installation():
    """Test if installation is working"""
    print("🧪 Testing installation...")
    
    try:
        # Test imports
        import streamlit
        import langchain
        import groq
        import whisper
        import sounddevice
        import pydantic
        
        print("✅ All core dependencies imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def main():
    """Main setup function"""
    print("🏥 Arovia - AI Health Desk Agent Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Test installation
    if not test_installation():
        print("⚠️  Installation test failed, but you can try running the app")
    
    print("\n✅ Setup completed!")
    print("\n🚀 Next steps:")
    print("1. Copy env.example to .env")
    print("2. Add your GROQ_API_KEY to .env")
    print("3. Run: streamlit run app.py")
    print("4. Or test: python test_triage.py")


if __name__ == "__main__":
    main()
