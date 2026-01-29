from typing import List, Optional
from sqlalchemy import select
from datetime import datetime
from database.database import db
from database.models import Question


class QuestionService:
    """Service for question operations"""

    async def create_question(
        self,
        from_user_id: int,
        from_username: Optional[str],
        question_text: str
    ) -> Question:
        """Create a new question"""
        async with db.get_session() as session:
            question = Question(
                from_user_id=from_user_id,
                from_username=from_username,
                question_text=question_text
            )
            session.add(question)
            await session.flush()
            await session.refresh(question)
            return question

    async def answer_question(
        self,
        question_id: int,
        answer_text: str,
        answered_by_user_id: int
    ) -> Optional[Question]:
        """Answer a question"""
        async with db.get_session() as session:
            result = await session.execute(
                select(Question).where(Question.id == question_id)
            )
            question = result.scalar_one_or_none()

            if question:
                question.answer_text = answer_text
                question.answered_at = datetime.utcnow()
                question.answered_by_user_id = answered_by_user_id
                await session.flush()
                await session.refresh(question)

            return question

    async def get_pending_questions(self) -> List[Question]:
        """Get all unanswered questions"""
        async with db.get_session() as session:
            result = await session.execute(
                select(Question)
                .where(Question.answer_text.is_(None))
                .order_by(Question.created_at.asc())
            )
            return result.scalars().all()

    async def get_question_by_id(self, question_id: int) -> Optional[Question]:
        """Get question by ID"""
        async with db.get_session() as session:
            result = await session.execute(
                select(Question).where(Question.id == question_id)
            )
            return result.scalar_one_or_none()


question_service = QuestionService()
