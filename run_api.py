#!/usr/bin/env python3
"""
Startup script for Arovia Health Desk API
"""
import sys
import os
import uvicorn
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Run the FastAPI server"""
    print("🏥 Starting Arovia Health Desk API...")
    print("📡 API will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔧 Alternative docs: http://localhost:8000/redoc")
    print("-" * 50)
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()
