"""Service for sending wedding reminder notifications"""
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo
from typing import Optional

from telegram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import Config
from database.database import db
from database.models import BotUser


# Московский часовой пояс
MSK_ZONE = ZoneInfo("Europe/Moscow")


class ReminderService:
    """Service for managing wedding reminders"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(timezone=MSK_ZONE)
        self._sent_reminders = set()  # Track sent reminders to avoid duplicates

    def start(self):
        """Start the reminder scheduler"""
        # Check every hour for upcoming reminders
        self.scheduler.add_job(
            self._check_and_send_reminders,
            'interval',
            hours=1,
            id='check_reminders',
            replace_existing=True
        )
        self.scheduler.start()
        print("📅 Reminder scheduler started!")

    def stop(self):
        """Stop the reminder scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            print("📅 Reminder scheduler stopped!")

    async def _check_and_send_reminders(self):
        """Check if we need to send any reminders"""
        today = date.today()
        wedding_date = Config.WEDDING_DATE

        # Calculate days until wedding
        days_until = (wedding_date - today).days

        # Define reminder milestones
        reminders = []
        if days_until == 30:
            reminders.append(("month", "📅 **1 месяц до свадьбы!**\n\n"))
        elif days_until == 7:
            reminders.append(("week", "📅 **1 неделя до свадьбы!**\n\n"))
        elif days_until == 1:
            reminders.append(("day", "🎊 **Завтра свадьба!**\n\n"))

        # Send reminders if any
        for reminder_type, prefix in reminders:
            reminder_key = f"{wedding_date.isoformat()}_{reminder_type}"
            if reminder_key not in self._sent_reminders:
                await self._send_reminder_to_all(prefix, days_until)
                self._sent_reminders.add(reminder_key)

    async def _send_reminder_to_all(self, message_prefix: str, days_until: int):
        """Send reminder to all subscribed bot users"""
        wedding_date = Config.WEDDING_DATE
        wedding_time = Config.WEDDING_TIME

        message = f"""{message_prefix}💍 До нашей свадьбы осталось **{days_until} дней**!

📆 **Дата:** {wedding_date.strftime('%d.%m.%Y')}
🕐 **Время:** {wedding_time}

📍 Будем очень рады видеть вас!

Если у вас есть вопросы, не стесняйтесь задавать их через бота 🤗
"""

        async with db.get_session() as session:
            from sqlalchemy import select
            result = await session.execute(
                select(BotUser).where(
                    BotUser.subscribed_to_reminders == True,
                    BotUser.is_active == True
                )
            )
            users = result.scalars().all()

        for user in users:
            try:
                await self.bot.send_message(
                    chat_id=user.user_id,
                    text=message,
                    parse_mode="Markdown"
                )
                print(f"✅ Reminder sent to {user.first_name or user.username or user.user_id}")
            except Exception as e:
                print(f"❌ Failed to send reminder to {user.user_id}: {e}")

    async def send_test_reminder(self, user_id: int):
        """Send a test reminder (for admin testing)"""
        message = """📅 **Тестовое напоминание**

Это тестовое сообщение для проверки системы напоминаний.

💍 До свадьбы осталось **{} дней**!

📆 Дата: {}
🕐 Время: {}
""".format(
            (Config.WEDDING_DATE - date.today()).days,
            Config.WEDDING_DATE.strftime('%d.%m.%Y'),
            Config.WEDDING_TIME
        )

        try:
            await self.bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode="Markdown"
            )
            return True
        except Exception as e:
            print(f"❌ Failed to send test reminder: {e}")
            return False
