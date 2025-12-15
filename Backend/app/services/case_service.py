from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.case import Case
from app.models.wallet import Wallet

class CaseService:

    async def create_case(self, session: AsyncSession, user_id: int, data):
        case = Case(
            title=data.title,
            description=data.description,
            user_id=user_id,
        )
        session.add(case)
        await session.commit()
        await session.refresh(case)
        return case

    async def attach_wallets(self, session: AsyncSession, case: Case, wallet_ids):
        result = await session.execute(
            select(Wallet).where(Wallet.id.in_(wallet_ids))
        )
        wallets = result.scalars().all()

        if not wallets:
            raise ValueError("No valid wallets found")

        case.wallets.extend(wallets)
        await session.commit()
        await session.refresh(case)
        return case

case_service = CaseService()
