"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.api.v1 import auth, projects, upload, modeling, ai_chat, firebase_auth


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    redoc_url=f"{settings.API_V1_PREFIX}/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Health status
    """
    return {"status": "healthy", "version": settings.VERSION}


# Include API routers
app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_PREFIX}/auth",
    tags=["Authentication"]
)

app.include_router(
    projects.router,
    prefix=f"{settings.API_V1_PREFIX}/projects",
    tags=["Projects"]
)

app.include_router(
    upload.router,
    prefix=f"{settings.API_V1_PREFIX}/upload",
    tags=["File Upload"]
)

app.include_router(
    modeling.router,
    prefix=f"{settings.API_V1_PREFIX}/modeling",
    tags=["Financial Modeling"]
)

app.include_router(
    ai_chat.router,
    prefix=f"{settings.API_V1_PREFIX}/ai",
    tags=["AI Assistant"]
)

app.include_router(
    firebase_auth.router,
    prefix=f"{settings.API_V1_PREFIX}/auth",
    tags=["Firebase Authentication"]
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors.
    
    Args:
        request: Request object
        exc: Exception
    
    Returns:
        JSON error response
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
                "details": str(exc) if settings.ENVIRONMENT == "development" else None
            }
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )
