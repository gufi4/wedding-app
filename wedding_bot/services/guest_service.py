from typing import List, Optional
from sqlalchemy import select
from database.database import db
from database.models import Guest


class GuestService:
    """Service for guest operations"""

    async def create_guest(
        self,
        name: str,
        guest_count: int,
        confirmation_status: str,
        comment: Optional[str] = None
    ) -> Guest:
        """Create a new guest"""
        async with db.get_session() as session:
            guest = Guest(
                name=name,
                guest_count=guest_count,
                confirmation_status=confirmation_status,
                comment=comment
            )
            session.add(guest)
            await session.flush()
            await session.refresh(guest)
            return guest

    async def get_all_guests(self) -> List[Guest]:
        """Get all guests"""
        async with db.get_session() as session:
            result = await session.execute(select(Guest).order_by(Guest.created_at.desc()))
            return result.scalars().all()

    async def get_guest_by_id(self, guest_id: int) -> Optional[Guest]:
        """Get guest by ID"""
        async with db.get_session() as session:
            result = await session.execute(select(Guest).where(Guest.id == guest_id))
            return result.scalar_one_or_none()

    async def get_confirmed_guests_count(self) -> int:
        """Get count of confirmed guests"""
        async with db.get_session() as session:
            result = await session.execute(
                select(Guest).where(Guest.confirmation_status == 'confirmed')
            )
            return len(result.scalars().all())


guest_service = GuestService()
