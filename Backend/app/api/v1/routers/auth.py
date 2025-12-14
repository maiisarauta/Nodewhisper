from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_async_session
from app.models.user import User
from app.api.v1.schemas.auth import RegisterUser, LoginUser, TokenResponse
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth")

@router.post("/register", response_model=TokenResponse)
async def register(payload: RegisterUser, session: AsyncSession = Depends(get_async_session)):

    query = select(User).where(User.email == payload.email)
    result = await session.execute(query)
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = auth_service.hash_password(payload.password)
    user = User(email=payload.email, username=payload.username, hashed_password=hashed)

    session.add(user)
    await session.commit()
    await session.refresh(user)

    token = auth_service.create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token)

@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginUser,
    session: AsyncSession = Depends(get_async_session)
):
    query = select(User).where(User.email == payload.email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not auth_service.verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = auth_service.create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token)
