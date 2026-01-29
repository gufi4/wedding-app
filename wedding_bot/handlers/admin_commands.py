from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.ext import ContextTypes
from config import Config
from services.guest_service import guest_service

# Московский часовой пояс
MSK_ZONE = ZoneInfo("Europe/Moscow")


class AdminHandler:
    """Handle admin commands"""

    async def guests_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /guests command - show all guests"""
        user_id = update.effective_user.id

        # Check if user is admin
        if not Config.is_admin(user_id):
            await update.message.reply_text("⛔ У вас нет прав для выполнения этой команды.")
            return

        guests = await guest_service.get_all_guests()

        if not guests:
            await update.message.reply_text("📋 Список гостей пуст.")
            return

        # Calculate statistics
        total_guests = sum(g.guest_count for g in guests)

        # Build message
        message = f"<b>📊 Гости</b>\n\n"
        message += f"Всего гостей: {total_guests}\n\n"
        message += "<b>📋 Список гостей:</b>\n\n"

        for guest in guests:
            message += f"• <b>{guest.name}</b> (Гостей: {guest.guest_count})\n"

            if guest.comment:
                message += f"   💬 {guest.comment}\n"

            # Convert to Moscow timezone
            created_at_msk = guest.created_at.replace(tzinfo=timezone.utc).astimezone(MSK_ZONE)
            message += f"   🕐 {created_at_msk.strftime('%d.%m.%Y %H:%M')}\n\n"

        # Split message if too long
        if len(message) > 4000:
            messages = [message[i:i+4000] for i in range(0, len(message), 4000)]
            for msg in messages:
                await update.message.reply_text(msg, parse_mode="HTML")
        else:
            await update.message.reply_text(message, parse_mode="HTML")

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command - show quick statistics"""
        user_id = update.effective_user.id

        if not Config.is_admin(user_id):
            await update.message.reply_text("⛔ У вас нет прав для выполнения этой команды.")
            return

        guests = await guest_service.get_all_guests()

        total_guests = sum(g.guest_count for g in guests)

        message = f"<b>📊 Статистика</b>\n\n"
        message += f"👥 Всего гостей: {total_guests}"

        await update.message.reply_text(message, parse_mode="HTML")


admin_handler = AdminHandler()
