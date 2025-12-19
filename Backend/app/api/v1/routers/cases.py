from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.db.session import get_async_session
from app.api.v1.deps import get_current_user
from app.models.case import Case
from app.models.case_wallet import CaseWallet
from app.models.wallet import Wallet
from app.models.user import User
from app.api.v1.schemas.case import CaseCreate, CaseOut
from app.api.v1.schemas.wallet import WalletOut
from app.api.v1.schemas.case_wallet import AttachWalletEvidenceSchema

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
async def attach_wallet_to_case(
    case_id: int,
    payload: AttachWalletEvidenceSchema,
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(
        select(Case).where(Case.id == case_id)
    )
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    wallet = await session.get(Wallet, payload.wallet_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    link = CaseWallet(
        case_id=case.id,
        wallet_id=wallet.id,
        confidence=payload.confidence,
        note=payload.note,
        source=payload.source,
    )

    session.add(link)
    await session.commit()

    return {"message": "Wallet linked with evidence"}

@router.get("/{case_id}/wallets")
async def get_case_wallets(
    case_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(
        select(CaseWallet)
        .where(CaseWallet.case_id == case_id)
        .options(selectinload(CaseWallet.wallet))
    )
    links = result.scalars().all()

    return [
        {
            "wallet": WalletOut.from_orm(link.wallet),
            "confidence": link.confidence,
            "note": link.note,
            "source": link.source,
            "created_at": link.created_at,
        }
        for link in links
    ]

@router.delete("/{case_id}/wallets/{wallet_id}")
async def detach_wallet_from_case(
    case_id: int,
    wallet_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(
        select(CaseWallet).where(
            CaseWallet.case_id == case_id,
            CaseWallet.wallet_id == wallet_id,
        )
    )
    link = result.scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    await session.delete(link)
    await session.commit()

    return {"message": "Wallet evidence removed"}
