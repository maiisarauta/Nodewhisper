from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.wallet import Wallet
from app.models.user import User

class WalletService:

    async def create_wallet(
        self,
        session: AsyncSession,
        user: User,
        address: str,
        label: str | None
    ):
        wallet = Wallet(
            address=address,
            label=label,
            user_id=user.id
        )
        session.add(wallet)
        await session.commit()
        await session.refresh(wallet)
        return wallet

    async def get_wallets(
        self,
        session: AsyncSession,
        user: User
    ):
        result = await session.execute(
            select(Wallet).where(Wallet.user_id == user.id)
        )
        return result.scalars().all()

    async def get_wallet(
        self,
        session: AsyncSession,
        user: User,
        wallet_id: int
    ):
        result = await session.execute(
            select(Wallet).where(
                Wallet.id == wallet_id,
                Wallet.user_id == user.id
            )
        )
        wallet = result.scalar_one_or_none()
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")
        return wallet

    async def update_wallet(
        self,
        session: AsyncSession,
        user: User,
        wallet_id: int,
        label: str | None,
        is_flagged: bool | None
    ):
        wallet = await self.get_wallet(session, user, wallet_id)

        if label is not None:
            wallet.label = label
        if is_flagged is not None:
            wallet.is_flagged = is_flagged

        await session.commit()
        await session.refresh(wallet)
        return wallet

wallet_service = WalletService()
