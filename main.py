# main.py
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.logger import init_loggers
from core.config import settings
from api.routes import register_routes 

# Initialize logging first
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    init_loggers()
    print("App is starting up...")
    yield
    print("App is shutting down...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    openapi_url=settings.OPENAPI_URL,
    lifespan=lifespan, 
)

# Security headers (you may add additional custom middleware for security headers here)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# **Register Routes**
register_routes(app)

if __name__ == "__main__":
    # Use a production-ready server (e.g., gunicorn with uvicorn workers)
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=False)
