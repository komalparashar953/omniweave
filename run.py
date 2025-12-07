import uvicorn
import os
import sys

if __name__ == "__main__":
    # Ensure the current directory is in sys.path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    print("Starting Universal Scraper with custom event loop policy for Windows compatibility...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
