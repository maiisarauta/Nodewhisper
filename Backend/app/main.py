import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import settings
from app.api.v1.routers import auth, wallets, cases, ws
from app.db.session import get_async_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 NodeWhisper backend starting...")
    yield
    print("🛑 NodeWhisper backend shutting down...")


def create_app() -> FastAPI:
    app = FastAPI(
        title="NodeWhisper Backend",
        version="1.0.0",
        description="API backend for NodeWhisper",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
    app.include_router(wallets.router, prefix="/api/v1", tags=["Wallets"])
    app.include_router(cases.router, prefix="/api/v1", tags=["Cases"])
    app.include_router(ws.router, prefix="/api/v1", tags=["WebSocket"])

    @app.get("/", tags=["Health"])
    async def root():
        return {
            "status": "running",
            "project": "NodeWhisper",
            "debug": settings.DEBUG,
            "version": "1.0.0",
        }

    @app.get("/db-check", tags=["Health"])
    async def db_check():
        async for session in get_async_session():
            result = await session.execute(text("SELECT 1"))
            return {"status": "ok", "db": result.scalar()}

    return app


app = create_app()
