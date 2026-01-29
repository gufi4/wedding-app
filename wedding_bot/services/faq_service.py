from typing import List, Optional
from sqlalchemy import select, delete
from database.database import db
from database.models import FAQ


class FAQService:
    """Service for FAQ operations"""

    async def get_all_faqs(self) -> List[FAQ]:
        """Get all FAQ items ordered by order field"""
        async with db.get_session() as session:
            result = await session.execute(
                select(FAQ).order_by(FAQ.order.asc())
            )
            return result.scalars().all()

    async def get_faq_by_id(self, faq_id: int) -> Optional[FAQ]:
        """Get FAQ by ID"""
        async with db.get_session() as session:
            result = await session.execute(
                select(FAQ).where(FAQ.id == faq_id)
            )
            return result.scalar_one_or_none()

    async def create_faq(
        self,
        question: str,
        answer: str,
        order: int
    ) -> FAQ:
        """Create a new FAQ item"""
        async with db.get_session() as session:
            faq = FAQ(
                question=question,
                answer=answer,
                order=order
            )
            session.add(faq)
            await session.flush()
            await session.refresh(faq)
            return faq

    async def update_faq(
        self,
        faq_id: int,
        question: str,
        answer: str
    ) -> Optional[FAQ]:
        """Update an FAQ item"""
        async with db.get_session() as session:
            result = await session.execute(
                select(FAQ).where(FAQ.id == faq_id)
            )
            faq = result.scalar_one_or_none()

            if faq:
                faq.question = question
                faq.answer = answer
                await session.flush()
                await session.refresh(faq)

            return faq

    async def delete_faq(self, faq_id: int) -> bool:
        """Delete an FAQ item"""
        async with db.get_session() as session:
            result = await session.execute(
                select(FAQ).where(FAQ.id == faq_id)
            )
            faq = result.scalar_one_or_none()

            if faq:
                await session.execute(
                    delete(FAQ).where(FAQ.id == faq_id)
                )
                return True

            return False

    async def get_next_order(self) -> int:
        """Get the next order number"""
        async with db.get_session() as session:
            result = await session.execute(
                select(FAQ).order_by(FAQ.order.desc()).limit(1)
            )
            faq = result.scalar_one_or_none()
            return (faq.order + 1) if faq else 0


faq_service = FAQService()
