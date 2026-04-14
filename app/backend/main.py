"""FastAPI backend for the AI Hedge Fund application.

This module serves as the main entry point for the backend API,
providing endpoints for portfolio analysis, stock data, and AI-driven
investment recommendations.
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Application lifespan
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    print("Starting AI Hedge Fund backend...")
    yield
    # Shutdown
    print("Shutting down AI Hedge Fund backend...")


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------

def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    app = FastAPI(
        title="AI Hedge Fund API",
        description=(
            "Backend API for the AI Hedge Fund — providing portfolio analysis, "
            "market data, and AI-driven investment signals."
        ),
        version="0.1.0",
        lifespan=lifespan,
        # Enable docs in all environments for personal/learning use
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # -----------------------------------------------------------------------
    # CORS
    # -----------------------------------------------------------------------
    allowed_origins = os.getenv(
        "ALLOWED_ORIGINS",
        # Added port 8080 as I sometimes run the frontend dev server there
        "http://localhost:3000,http://127.0.0.1:3000,http://localhost:8080",
    ).split(",")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # -----------------------------------------------------------------------
    # Routers  (imported lazily so missing deps surface early)
    # -----------------------------------------------------------------------
    from app.backend.routers import health  # noqa: PLC0415

    app.include_router(health.router, prefix="/api", tags=["health"])

    return app


# Module-level app instance used by uvicorn / gunicorn
app = create_app()


# ---------------------------------------------------------------------------
# Dev entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.backend.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("RELOAD", "true").lower() == "true",
        log_level=os.getenv("LOG_LEVEL", "info"),
    )
