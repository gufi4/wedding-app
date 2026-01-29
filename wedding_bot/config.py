import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""

    # Telegram Bot Token
    BOT_TOKEN = os.getenv("API_TOKEN")

    # Telegram User IDs
    BRIDE_ID = int(os.getenv("BRIDE_ID", "123456789"))  # TEST_BRIDE_ID placeholder
    GROOM_ID = int(os.getenv("GROOM_ID", "987654321"))  # TEST_GROOM_ID placeholder

    # Admin IDs (list of telegram user IDs)
    ADMIN_IDS = [
        int(id.strip()) for id in os.getenv("ADMIN_IDS", "123456789,987654321").split(",")
    ]

    # Website Bot ID - receives messages from website form via Telegram API
    WEBSITE_BOT_ID = int(os.getenv("WEBSITE_BOT_ID", "123456789"))

    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///wedding_bot.db")

    # API Configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8080"))

    # Wedding Date
    WEDDING_DATE = datetime.strptime(os.getenv("WEDDING_DATE", "2026-04-25"), "%Y-%m-%d").date()
    WEDDING_TIME = os.getenv("WEDDING_TIME", "15:00")

    # Bot Settings
    GUEST_QUESTION_BUTTON_TEXT = "Задать вопрос"
    FAQ_BUTTON_TEXT = "Частые вопросы"
    ADMIN_GUESTS_BUTTON_TEXT = "📋 Список гостей"
    ADMIN_STATS_BUTTON_TEXT = "📊 Статистика"
    ADMIN_EDIT_FAQ_BUTTON_TEXT = "✏️ Редактировать FAQ"

    @classmethod
    def is_admin(cls, user_id: int) -> bool:
        """Check if user is admin"""
        return user_id in cls.ADMIN_IDS

    @classmethod
    def is_website_sender(cls, user_id: int) -> bool:
        """Check if message is from website"""
        return user_id == cls.WEBSITE_BOT_ID

    @classmethod
    def get_owners(cls) -> list:
        """Get bride and groom IDs"""
        return [cls.BRIDE_ID, cls.GROOM_ID]
