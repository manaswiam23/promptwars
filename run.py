import uvicorn
from app.config import settings

if __name__ == "__main__":
    print("=" * 65)
    print(f"  Starting {settings.PROJECT_NAME}")
    print(f"  Version: {settings.VERSION}")
    print(f"  Server URL: http://{settings.HOST}:{settings.PORT}")
    print(f"  Gemini API Key configured: {'YES' if settings.has_gemini_key else 'NO (Running in high-fidelity demo mode)'}")
    print("=" * 65)
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
