import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get port from environment variable or default to 8000
    port = int(os.getenv("PORT", 8000))
    
    print(f"Starting FastAPI server on port {port}")
    print("Access your API at:")
    print(f"  - Local: http://localhost:{port}")
    print(f"  - Health check: http://localhost:{port}/health")
    print(f"  - API docs: http://localhost:{port}/docs")
    print("  - Your ngrok URL will be shown when you run ngrok")
    
    # Run the server
    uvicorn.run(
        "app:app", 
        host="0.0.0.0", 
        port=port, 
        reload=False,  # Disable reload for production
        log_level="info"
    ) 