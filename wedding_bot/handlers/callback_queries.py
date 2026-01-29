from telegram import Update
from telegram.ext import ContextTypes
from config import Config
from services.question_service import question_service
from utils.keyboards import get_main_menu_keyboard


class CallbackQueryHandler:
    """Handle callback queries from inline keyboards"""

    def __init__(self):
        self.pending_answers = {}  # Store question_id waiting for answer

    async def answer_button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle answer button click from bride"""
        query = update.callback_query
        await query.answer()

        user_id = query.from_user.id

        # Only bride can answer
        if user_id != Config.BRIDE_ID:
            await query.edit_message_text("⛔ Только невеста может отвечать на вопросы.")
            return

        # Parse callback data: answer_{question_id}_{from_user_id}
        data = query.data
        parts = data.split('_')

        if len(parts) < 3:
            return

        question_id = int(parts[1])
        from_user_id = int(parts[2])

        # Store pending answer
        self.pending_answers[user_id] = {
            "question_id": question_id,
            "from_user_id": from_user_id
        }

        # Get question
        question = await question_service.get_question_by_id(question_id)

        await query.edit_message_text(
            f"💬 <b>Вопрос #{question_id}</b>\n\n"
            f"{question.question_text}\n\n"
            f"Пожалуйста, напишите ваш ответ:",
            parse_mode="HTML"
        )

    async def receive_answer_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Receive answer text from bride"""
        user_id = update.effective_user.id

        if user_id not in self.pending_answers:
            return False

        answer_text = update.message.text

        pending_data = self.pending_answers[user_id]
        question_id = pending_data["question_id"]
        from_user_id = pending_data["from_user_id"]

        # Save answer to database
        question = await question_service.answer_question(
            question_id=question_id,
            answer_text=answer_text,
            answered_by_user_id=user_id
        )

        if not question:
            await update.message.reply_text("❌ Ошибка: вопрос не найден.")
            del self.pending_answers[user_id]
            return False

        # Send answer to guest
        try:
            await context.bot.send_message(
                chat_id=from_user_id,
                text=f"Пришел ответ на твой вопрос\n\n❓ Вопрос:\n{question.question_text}\n\n💬 Ответ:\n{answer_text}",
                parse_mode="HTML"
            )
            await update.message.reply_text("✅ Ответ отправлен гостю!")
        except Exception as e:
            await update.message.reply_text(f"❌ Не удалось отправить ответ: {e}")

        # Remove from pending
        del self.pending_answers[user_id]
        return True


callback_query_handler = CallbackQueryHandler()
