#!/usr/bin/env python3
"""
Startup script for Arovia Health Desk Frontend
"""
import subprocess
import sys
import os
from pathlib import Path

def main():
    """Run the React frontend development server"""
    print("🎨 Starting Arovia Health Desk Frontend...")
    print("📱 Frontend will be available at: http://localhost:5173")
    print("🔗 Make sure the FastAPI backend is running on http://localhost:8000")
    print("-" * 50)
    
    # Change to frontend directory
    frontend_dir = Path(__file__).parent / "frontend"
    os.chdir(frontend_dir)
    
    try:
        # Start the development server
        subprocess.run(["npm", "run", "dev"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting frontend: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Frontend server stopped")
        sys.exit(0)

if __name__ == "__main__":
    main()
