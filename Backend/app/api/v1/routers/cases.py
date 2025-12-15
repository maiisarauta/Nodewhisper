from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.db.session import get_async_session
from app.api.v1.deps import get_current_user
from app.models.case import Case, case_wallets
from app.models.wallet import Wallet
from app.models.user import User
from app.api.v1.schemas.case import CaseCreate, CaseOut
from app.api.v1.schemas.wallet import WalletOut
from app.api.v1.schemas.case import AttachWalletsSchema

router = APIRouter(prefix="/cases")

@router.post("/", response_model=CaseOut)
async def create_case(
    payload: CaseCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    case = Case(
        title=payload.title,
        description=payload.description,
        user_id=current_user.id,
    )

    session.add(case)
    await session.commit()
    await session.refresh(case)

    return case

@router.post("/{case_id}/wallets")
async def attach_wallets_to_case(
    case_id: int,
    payload: AttachWalletsSchema,
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(
        select(Case)
        .where(Case.id == case_id)
        .options(selectinload(Case.wallets))
    )
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    wallets_result = await session.execute(
        select(Wallet).where(Wallet.id.in_(payload.wallet_ids))
    )
    wallets = wallets_result.scalars().all()

    if not wallets:
        raise HTTPException(status_code=404, detail="Wallets not found")

    case.wallets = wallets

    await session.commit()
    return {"message": "Wallets attached"}

@router.get("/{case_id}/wallets", response_model=list[WalletOut])
async def get_case_wallets(
    case_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    result = await session.execute(
        select(Case)
        .where(Case.id == case_id)
        .options(selectinload(Case.wallets))
    )
    case = result.scalar_one_or_none()

    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    return case.wallets

@router.delete("/{case_id}/wallets/{wallet_id}")
async def detach_wallet_from_case(
    case_id: int,
    wallet_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(
        select(Case)
        .where(Case.id == case_id)
        .options(selectinload(Case.wallets))
    )
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    wallet = next((w for w in case.wallets if w.id == wallet_id), None)
    if not wallet:
        raise HTTPException(status_code=404, detail="Link not found")

    case.wallets.remove(wallet)
    await session.commit()
    return {"message": "Wallet detached"}
