from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text

from app.core.config import settings
from app.api.v1.routers import wallets, auth, cases, ws
from app.db.session import get_async_session

app = FastAPI(
    title="NodeWhisper Backend",
    version="1.0.0",
    description="API backend for the NodeWhisper",
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Add Redis connection or background tasks here later
    print("🚀 NodeWhisper backend starting...")

@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 Shutting down NodeWhisper backend...")

@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "running",
        "project": "NodeWhisper",
        "debug": settings.DEBUG,
        "version": "1.0.0",
    }

@app.get("/db-check")
async def db_check():
    async for session in get_async_session():
        result = await session.execute(text("SELECT 1"))
        return {"status": "ok", "db": result.scalar()}

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(wallets.router, prefix="/api/v1", tags=["wallets"])
app.include_router(cases.router, prefix="/api/v1", tags=["cases"])
app.include_router(ws.router, prefix="/api/v1", tags=["ws"])
