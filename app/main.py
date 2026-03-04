import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import api
from app.config import settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Startup complete.")
    yield
    logger.info("Shutting down.")


app = FastAPI(
    title="AI Research Synthesis Engine API",
    description="University research paper retrieval, analysis, and gap identification system",
    version="2.0.0",
    lifespan=lifespan,
)

app.include_router(api.router, prefix="/api")

import os
os.makedirs(settings.PDF_OUTPUT_DIR, exist_ok=True)
app.mount("/pdfs", StaticFiles(directory=settings.PDF_OUTPUT_DIR), name="pdfs")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}