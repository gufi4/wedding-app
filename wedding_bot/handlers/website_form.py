import json
from telegram import Update
from telegram.ext import ContextTypes
from config import Config
from services.guest_service import guest_service
from services.notification_service import NotificationService


class WebsiteFormHandler:
    """Handle messages from website form sent via Telegram API"""

    def __init__(self):
        self.notification_service = None  # Will be set with bot instance

    def set_bot(self, bot):
        """Set bot instance for notifications"""
        self.notification_service = NotificationService(bot)

    async def handle_website_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process JSON message from website"""
        user_id = update.effective_user.id

        # Verify message is from website
        if not Config.is_website_sender(user_id):
            return False

        try:
            # Parse JSON from message text
            message_text = update.message.text
            data = json.loads(message_text)

            # Validate required fields
            required_fields = ["name", "guest_count", "confirmation_status"]
            for field in required_fields:
                if field not in data:
                    await update.message.reply_text(
                        f"❌ Ошибка: отсутствует поле '{field}'"
                    )
                    return True

            name = data["name"]
            guest_count = int(data["guest_count"])
            confirmation_status = data["confirmation_status"]
            comment = data.get("comment", "")

            # Validate confirmation status
            valid_statuses = ["confirmed", "declined", "pending"]
            if confirmation_status not in valid_statuses:
                await update.message.reply_text(
                    f"❌ Ошибка: invalid confirmation_status. Must be one of: {valid_statuses}"
                )
                return True

            # Create guest in database
            guest = await guest_service.create_guest(
                name=name,
                guest_count=guest_count,
                confirmation_status=confirmation_status,
                comment=comment
            )

            # Notify bride and groom
            await self.notification_service.notify_about_new_guest(guest)

            # Send success confirmation
            await update.message.reply_text(
                f"✅ Гость успешно зарегистрирован!\n"
                f"ID: {guest.id}\n"
                f"Имя: {name}\n"
                f"Количество: {guest_count}\n"
                f"Статус: {confirmation_status}"
            )

            return True

        except json.JSONDecodeError:
            await update.message.reply_text(
                "❌ Ошибка: неверный формат JSON"
            )
            return True
        except Exception as e:
            await update.message.reply_text(
                f"❌ Ошибка при обработке: {str(e)}"
            )
            return True


website_form_handler = WebsiteFormHandler()
