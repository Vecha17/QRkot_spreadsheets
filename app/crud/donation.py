from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.donation import Donation

from .base import CRUDBase


class CRUDDonation(CRUDBase):

    async def get_by_user(
            self,
            user_id: int,
            session: AsyncSession
    ) -> list[Donation]:
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user_id,
            )
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
