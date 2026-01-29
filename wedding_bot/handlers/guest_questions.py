from telegram import Update
from telegram.ext import ContextTypes
from config import Config
from services.question_service import question_service
from utils.keyboards import get_main_menu_keyboard, get_answer_keyboard


class QuestionHandler:
    """Handle guest question button and conversation"""

    def __init__(self):
        self.user_questions = {}  # Temporary storage for pending questions

    async def question_button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle question button click"""
        user = update.effective_user

        # Store that user is in question mode
        self.user_questions[user.id] = {
            "username": user.username,
            "waiting_for_text": True
        }

        await update.message.reply_text(
            "Пожалуйста, напишите ваш вопрос:"
        )

    async def receive_question_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Receive question text from user"""
        user_id = update.effective_user.id

        if user_id not in self.user_questions:
            return False

        if not self.user_questions[user_id].get("waiting_for_text"):
            return False

        question_text = update.message.text

        # Save question to database
        question = await question_service.create_question(
            from_user_id=user_id,
            from_username=update.effective_user.username,
            question_text=question_text
        )

        # Send question to bride with answer button
        username = update.effective_user.username or "гостя"
        await context.bot.send_message(
            chat_id=Config.BRIDE_ID,
            text=f"Вопрос от @{username}\n\n{question_text}",
            reply_markup=get_answer_keyboard(question.id, user_id)
        )

        # Notify guest that question was sent
        await update.message.reply_text(
            "Спасибо! Ваш вопрос отправлен. Мы ответим вам в ближайшее время.",
            reply_markup=get_main_menu_keyboard()
        )

        # Remove from pending
        del self.user_questions[user_id]
        return True


question_handler = QuestionHandler()
