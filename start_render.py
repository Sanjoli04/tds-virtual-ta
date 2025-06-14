#!/usr/bin/env python3
"""
Production startup script for Render deployment
"""
import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get port from environment (Render sets this automatically)
    port = int(os.environ.get("PORT", 10000))
    
    # Production configuration
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        workers=1,  # Single worker for SQLite compatibility
        reload=False,  # No auto-reload in production
        log_level="info",
        access_log=True
    ) 