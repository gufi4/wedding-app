from datetime import timezone
from zoneinfo import ZoneInfo

from telegram import Bot
from config import Config
from database.models import Guest

# Московский часовой пояс
MSK_ZONE = ZoneInfo("Europe/Moscow")


class NotificationService:
    """Service for sending notifications"""

    def __init__(self, bot: Bot):
        self.bot = bot

    async def notify_about_new_guest(self, guest: Guest):
        """Notify bride and groom about new guest"""
        message = self._format_guest_message(guest)

        for user_id in Config.get_owners():
            try:
                await self.bot.send_message(
                    chat_id=user_id,
                    text=message,
                    parse_mode="HTML"
                )
            except Exception as e:
                print(f"Failed to notify user {user_id}: {e}")

    def _format_guest_message(self, guest: Guest) -> str:
        """Format guest notification message"""
        message = f"""<b>🎉 Новый гость!</b>

👤 <b>Имя:</b> {guest.name}
👥 <b>Количество гостей:</b> {guest.guest_count}
"""

        if guest.comment:
            message += f"💬 <b>Комментарий:</b> {guest.comment}\n"

        # Convert to Moscow timezone
        created_at_msk = guest.created_at.replace(tzinfo=timezone.utc).astimezone(MSK_ZONE)
        message += f"🕐 <b>Дата:</b> {created_at_msk.strftime('%d.%m.%Y %H:%M')}"

        return message
