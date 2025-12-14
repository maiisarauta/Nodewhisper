from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.api.v1.schemas.wallet import (
    WalletCreate,
    WalletUpdate,
    WalletOut
)
from app.services.wallet_service import wallet_service
from app.api.v1.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/wallets")


@router.post("/", response_model=WalletOut)
async def create_wallet(
    payload: WalletCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await wallet_service.create_wallet(
        session,
        current_user,
        payload.address,
        payload.label
    )


@router.get("/", response_model=list[WalletOut])
async def list_wallets(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await wallet_service.get_wallets(session, current_user)


@router.get("/{wallet_id}", response_model=WalletOut)
async def get_wallet(
    wallet_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await wallet_service.get_wallet(
        session,
        current_user,
        wallet_id
    )


@router.put("/{wallet_id}", response_model=WalletOut)
async def update_wallet(
    wallet_id: int,
    payload: WalletUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await wallet_service.update_wallet(
        session,
        current_user,
        wallet_id,
        payload.label,
        payload.is_flagged
    )
