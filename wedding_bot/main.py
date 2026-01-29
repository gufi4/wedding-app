import asyncio
import signal
import sys
import io
from datetime import datetime

# Fix Windows console encoding for emoji
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    # Fix for Windows: use SelectorEventLoopPolicy for aiosqlite compatibility
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import Config
from database.database import db
from database.models import BotUser
from handlers.guest_questions import question_handler
from handlers.admin_commands import admin_handler
from handlers.callback_queries import callback_query_handler
from handlers.website_form import website_form_handler
from handlers.admin_faq import admin_faq_handler
from utils.keyboards import get_main_menu_keyboard, get_admin_menu_keyboard
from services.reminder_service import ReminderService


class WeddingBot:
    """Main wedding bot application"""

    def __init__(self):
        self.application = None
        self.running = False
        self.http_runner = None
        self.reminder_service = None

    async def init(self):
        """Initialize the bot"""
        print("📦 Initializing database...", flush=True)
        # Initialize database
        await db.init_db()
        print("✅ Database initialized!", flush=True)

        print("🤖 Creating Telegram application...", flush=True)
        # Create application
        self.application = Application.builder().token(Config.BOT_TOKEN).build()
        print("✅ Application created!", flush=True)

        # Set bot instance for website form handler
        website_form_handler.set_bot(self.application.bot)

        # Initialize reminder service
        print("📅 Initializing reminder service...", flush=True)
        self.reminder_service = ReminderService(self.application.bot)
        self.reminder_service.start()
        print("✅ Reminder service initialized!", flush=True)

        print("📝 Registering handlers...", flush=True)
        # Register handlers
        self._register_handlers()
        print("✅ Handlers registered!", flush=True)

        print("✅ Bot initialized successfully!", flush=True)

    def _register_handlers(self):
        """Register all command and message handlers"""

        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("guests", admin_handler.guests_command))
        self.application.add_handler(CommandHandler("stats", admin_handler.stats_command))
        self.application.add_handler(CommandHandler("test_reminder", self.test_reminder_command))

        # Callback query handlers
        self.application.add_handler(CallbackQueryHandler(
            callback_query_handler.answer_button_handler,
            pattern="^answer_"
        ))

        # FAQ callback handlers
        self.application.add_handler(CallbackQueryHandler(
            admin_faq_handler.faq_list_callback,
            pattern="^faq_list$"
        ))
        self.application.add_handler(CallbackQueryHandler(
            admin_faq_handler.faq_add_callback,
            pattern="^faq_add$"
        ))
        self.application.add_handler(CallbackQueryHandler(
            admin_faq_handler.faq_edit_callback,
            pattern="^faq_edit_"
        ))
        self.application.add_handler(CallbackQueryHandler(
            admin_faq_handler.faq_delete_callback,
            pattern="^faq_delete_"
        ))
        self.application.add_handler(CallbackQueryHandler(
            admin_faq_handler.faq_back_callback,
            pattern="^faq_back$"
        ))
        self.application.add_handler(CallbackQueryHandler(
            admin_faq_handler.faq_exit_callback,
            pattern="^faq_exit$"
        ))

        # Message handlers for receiving questions, answers and website form data
        self.application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            self.handle_text_message
        ))

    async def _save_bot_user(self, user):
        """Save or update bot user in database"""
        async with db.get_session() as session:
            from sqlalchemy import select
            result = await session.execute(
                select(BotUser).where(BotUser.user_id == user.id)
            )
            bot_user = result.scalar_one_or_none()

            if bot_user:
                # Update existing user
                bot_user.username = user.username
                bot_user.first_name = user.first_name
                bot_user.last_name = user.last_name
                bot_user.last_interaction = datetime.utcnow()
            else:
                # Create new user
                bot_user = BotUser(
                    user_id=user.id,
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    subscribed_to_reminders=True  # Default to subscribed
                )
                session.add(bot_user)

            await session.commit()

    async def start_command(self, update, context):
        """Handle /start command"""
        user = update.effective_user
        user_id = user.id

        # Save or update bot user
        await self._save_bot_user(user)

        # Check if user is admin
        is_admin = Config.is_admin(user_id)

        if is_admin:
            welcome_message = f"""👋 <b>Добро пожаловать, {user.first_name}!</b>

<b>Админ-панель</b>

Здесь вы можете:
• Просматривать список гостей
• Смотреть статистику
• Задавать вопросы
• Просматривать FAQ

Используйте кнопки ниже для навигации.
"""
            reply_markup = get_admin_menu_keyboard()
        else:
            welcome_message = f"""👋 <b>Добро пожаловать, {user.first_name}!</b>

Это бот для нашего свадебного праздника!

Здесь вы можете:
• Задать вопросы нам
• Посмотреть частые вопросы

Используйте кнопки ниже для навигации.
"""
            reply_markup = get_main_menu_keyboard()

        await update.message.reply_text(
            welcome_message,
            parse_mode="HTML",
            reply_markup=reply_markup
        )

    async def help_command(self, update, context):
        """Handle /help command"""
        user_id = update.effective_user.id
        is_admin = Config.is_admin(user_id)

        if is_admin:
            help_text = """<b>📖 Справка (Админ)</b>

<b>Доступные функции:</b>
• 📋 Список гостей - Показать всех гостей
• 📊 Статистика - Быстрая статистика
• Задать вопрос - Задать вопрос нам
• Частые вопросы - Просмотр FAQ

<b>Команды (все также работают):</b>
• /guests - Список гостей
• /stats - Статистика

Используйте кнопки для быстрого доступа! 👇
"""
            keyboard = get_admin_menu_keyboard()
        else:
            help_text = """<b>📖 Справка</b>

<b>Для гостей:</b>
• Нажмите кнопку "Задать вопрос" чтобы задать вопрос
• Нажмите кнопку "Частые вопросы" для просмотра FAQ

Если у вас есть вопросы, просто нажмите кнопку ниже! 👇
"""
            keyboard = get_main_menu_keyboard()

        await update.message.reply_text(
            help_text,
            parse_mode="HTML",
            reply_markup=keyboard
        )

    async def test_reminder_command(self, update, context):
        """Test sending reminders to all subscribed bot users"""
        user_id = update.effective_user.id

        # Only admins can test reminders
        if not Config.is_admin(user_id):
            await update.message.reply_text("❌ Эта команда доступна только администраторам.")
            return

        if not self.reminder_service:
            await update.message.reply_text("❌ Сервис напоминаний не инициализирован.")
            return

        await update.message.reply_text("📅 Отправка тестовых уведомлений всем пользователям...")

        # Send test reminders to all subscribed users
        from datetime import date

        message = f"""📅 **Тестовое напоминание**

Это тестовое сообщение для проверки системы напоминаний.

💍 До свадьбы осталось **{(Config.WEDDING_DATE - date.today()).days} дней**!

📆 **Дата:** {Config.WEDDING_DATE.strftime('%d.%m.%Y')}
🕐 **Время:** {Config.WEDDING_TIME}
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

        sent_count = 0
        failed_count = 0

        for user in users:
            try:
                await self.application.bot.send_message(
                    chat_id=user.user_id,
                    text=message,
                    parse_mode="Markdown"
                )
                sent_count += 1
                print(f"✅ Test reminder sent to {user.first_name or user.username or user.user_id}")
            except Exception as e:
                failed_count += 1
                print(f"❌ Failed to send test reminder to {user.user_id}: {e}")

        await update.message.reply_text(
            f"✅ Рассылка завершена!\n\n"
            f"📊 Отправлено: {sent_count}\n"
            f"❌ Ошибок: {failed_count}\n"
            f"👥 Всего пользователей: {len(users)}"
        )

    async def handle_text_message(self, update, context):
        """Handle text messages"""
        user_id = update.effective_user.id
        message_text = update.message.text

        # Check if message is from website
        if Config.is_website_sender(user_id):
            await website_form_handler.handle_website_message(update, context)
            return

        # Check if user pressed "Задать вопрос" button
        if message_text == Config.GUEST_QUESTION_BUTTON_TEXT:
            await question_handler.question_button_handler(update, context)
            return

        # Check if user pressed "Частые вопросы" button
        if message_text == Config.FAQ_BUTTON_TEXT:
            await self.faq_handler(update, context)
            return

        # Admin buttons
        if Config.is_admin(user_id):
            if message_text == Config.ADMIN_GUESTS_BUTTON_TEXT:
                await admin_handler.guests_command(update, context)
                return
            if message_text == Config.ADMIN_STATS_BUTTON_TEXT:
                await admin_handler.stats_command(update, context)
                return
            if message_text == Config.ADMIN_EDIT_FAQ_BUTTON_TEXT:
                await admin_faq_handler.faq_edit_button_handler(update, context)
                return

        # Check if admin is adding FAQ
        if user_id in admin_faq_handler.adding_faq:
            handled = await admin_faq_handler.faq_add_receive_question(update, context)
            if handled:
                return
            handled = await admin_faq_handler.faq_add_receive_answer(update, context)
            if handled:
                return

        # Check if admin is editing FAQ
        if user_id in admin_faq_handler.editing_faq:
            handled = await admin_faq_handler.faq_edit_receive_question(update, context)
            if handled:
                return
            handled = await admin_faq_handler.faq_edit_receive_answer(update, context)
            if handled:
                return

        # Check if user is sending a question
        if user_id in question_handler.user_questions:
            await question_handler.receive_question_text(update, context)
            return

        # Check if user (bride) is sending an answer
        if user_id in callback_query_handler.pending_answers:
            await callback_query_handler.receive_answer_text(update, context)
            return

        # Otherwise, send help message
        keyboard = get_admin_menu_keyboard() if Config.is_admin(user_id) else get_main_menu_keyboard()
        await update.message.reply_text(
            "Пожалуйста, используйте кнопки меню для взаимодействия с ботом.",
            reply_markup=keyboard
        )

    async def faq_handler(self, update, context):
        """Handle FAQ button click"""
        from services.faq_service import faq_service

        user_id = update.effective_user.id
        is_admin = Config.is_admin(user_id)
        keyboard = get_admin_menu_keyboard() if is_admin else get_main_menu_keyboard()

        faqs = await faq_service.get_all_faqs()

        if not faqs:
            faq_message = "📚 <b>Частые вопросы</b>\n\nПока нет вопросов."
        else:
            lines = ["📚 <b>Частые вопросы</b>\n"]
            for faq in faqs:
                lines.append(f"\n❓ <b>{faq.question}</b>")
                lines.append(f"💬 {faq.answer}")
            faq_message = "\n".join(lines)

        await update.message.reply_text(
            faq_message,
            parse_mode="HTML",
            reply_markup=keyboard
        )

    async def run(self):
        """Run both HTTP server and Telegram bot concurrently"""
        self.running = True

        # Setup HTTP server first
        from api.server import create_http_server, setup_http_server
        self.http_runner = create_http_server(self.application.bot)
        await setup_http_server(self.http_runner)

        print("🌐 HTTP API server started!")

        # Initialize application
        await self.application.initialize()
        await self.application.start()

        print("🚀 Starting polling...")

        # Start polling
        await self.application.updater.start_polling(
            drop_pending_updates=True
        )

        print("✅ Polling is running!")

        # Keep bot running
        try:
            while self.running:
                await asyncio.sleep(1)
        except (KeyboardInterrupt, asyncio.CancelledError):
            print("\n⏹️ Stopping bot...")
        finally:
            await self.shutdown()

    async def shutdown(self):
        """Shutdown the bot and HTTP server"""
        print("🛑 Shutting down...")
        self.running = False

        # Stop reminder service
        if self.reminder_service:
            self.reminder_service.stop()

        # Cleanup HTTP server
        if self.http_runner:
            await self.http_runner.cleanup()

        # Cleanup Telegram bot
        if self.application:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()

        print("✅ Shutdown complete!")


async def main_async():
    """Async main entry point"""
    print("Creating bot instance...", flush=True)
    bot = WeddingBot()
    print("Initializing bot...", flush=True)
    await bot.init()
    print("Running bot...", flush=True)
    await bot.run()


def main():
    """Main entry point"""
    print("Starting bot...", flush=True)
    try:
        # Run bot
        asyncio.run(main_async())
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
