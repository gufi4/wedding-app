from sqlalchemy import Column, Integer, String, Text, DateTime, BigInteger, Boolean
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all models"""
    pass


class BotUser(Base):
    """Bot user model - tracks users who started the bot"""
    __tablename__ = "bot_users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, unique=True)  # Telegram user ID
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)  # For blocking/unblocking users
    subscribed_to_reminders = Column(Boolean, default=True)  # Subscribe to wedding reminders
    created_at = Column(DateTime, default=datetime.utcnow)
    last_interaction = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_active": self.is_active,
            "subscribed_to_reminders": self.subscribed_to_reminders,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Guest(Base):
    """Guest model"""
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    guest_count = Column(Integer, nullable=False, default=1)
    confirmation_status = Column(String(50), nullable=False, default='pending')
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "guest_count": self.guest_count,
            "confirmation_status": self.confirmation_status,
            "comment": self.comment,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Question(Base):
    """Question model"""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    from_user_id = Column(BigInteger, nullable=False)
    from_username = Column(String(255), nullable=True)
    question_text = Column(Text, nullable=False)
    answer_text = Column(Text, nullable=True)
    answered_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    answered_by_user_id = Column(BigInteger, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "from_user_id": self.from_user_id,
            "from_username": self.from_username,
            "question_text": self.question_text,
            "answer_text": self.answer_text,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "answered_at": self.answered_at.isoformat() if self.answered_at else None
        }


class FAQ(Base):
    """FAQ model"""
    __tablename__ = "faq_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String(500), nullable=False)
    answer = Column(Text, nullable=False)
    order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "order": self.order,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
