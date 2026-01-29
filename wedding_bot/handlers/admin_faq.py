from telegram import Update
from telegram.ext import ContextTypes
from config import Config
from services.faq_service import faq_service
from utils.keyboards import get_faq_management_keyboard, get_faq_list_keyboard


class AdminFAQHandler:
    """Handle admin FAQ editing"""

    def __init__(self):
        self.adding_faq = {}  # {user_id: {step: 'question'|'answer', question: '...'}}
        self.editing_faq = {}  # {user_id: {step: 'question'|'answer', faq_id: id, new_question: '...'}}
        self.faq_locks = {}  # {faq_id: user_id} - track which FAQ is being edited by whom

    async def faq_edit_button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle FAQ edit button click"""
        user_id = update.effective_user.id

        if not Config.is_admin(user_id):
            await update.message.reply_text("⛔ У вас нет прав для редактирования FAQ.")
            return

        faqs = await faq_service.get_all_faqs()

        if not faqs:
            message = """📝 <b>Редактирование FAQ</b>

Список пуст. Нажмите \"➕ Добавить\" чтобы создать первый вопрос."""
            keyboard = get_faq_management_keyboard(empty=True)
        else:
            message = f"""📝 <b>Редактирование FAQ</b>

Всего вопросов: {len(faqs)}

Выберите действие:"""
            keyboard = get_faq_management_keyboard(empty=False)

        await update.message.reply_text(
            message,
            parse_mode="HTML",
            reply_markup=keyboard
        )

    async def faq_list_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle FAQ list callback"""
        query = update.callback_query
        await query.answer()

        user_id = query.from_user.id

        if not Config.is_admin(user_id):
            await query.edit_message_text("⛔ У вас нет прав.")
            return

        faqs = await faq_service.get_all_faqs()

        if not faqs:
            message = "📋 Список FAQ пуст.\n\nНажмите \"➕ Добавить\" чтобы создать первый вопрос."
            keyboard = get_faq_management_keyboard(empty=True)
        else:
            lines = ["📋 <b>Список FAQ:</b>\n"]
            for faq in faqs:
                short_answer = faq.answer[:50] + "..." if len(faq.answer) > 50 else faq.answer
                lines.append(f"\n#{faq.id} <b>{faq.question}</b>")
                lines.append(f"   {short_answer}")

            message = "\n".join(lines)
            keyboard = get_faq_list_keyboard(faqs)

        await query.edit_message_text(
            message,
            parse_mode="HTML",
            reply_markup=keyboard
        )

    async def faq_add_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle add FAQ callback"""
        query = update.callback_query
        await query.answer()

        user_id = query.from_user.id

        if not Config.is_admin(user_id):
            await query.edit_message_text("⛔ У вас нет прав.")
            return

        self.adding_faq[user_id] = {"step": "question"}

        await query.edit_message_text(
            "➕ <b>Добавление FAQ</b>\n\nВведите вопрос:",
            parse_mode="HTML"
        )

    async def faq_add_receive_question(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Receive question text for new FAQ"""
        user_id = update.effective_user.id

        if user_id not in self.adding_faq:
            return False

        data = self.adding_faq[user_id]
        if data.get("step") != "question":
            return False

        question_text = update.message.text

        self.adding_faq[user_id]["step"] = "answer"
        self.adding_faq[user_id]["question"] = question_text

        await update.message.reply_text(
            f"❓ Вопрос: <b>{question_text}</b>\n\nВведите ответ:",
            parse_mode="HTML"
        )
        return True

    async def faq_add_receive_answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Receive answer text for new FAQ"""
        user_id = update.effective_user.id

        if user_id not in self.adding_faq:
            return False

        data = self.adding_faq[user_id]
        if data.get("step") != "answer":
            return False

        answer_text = update.message.text
        question_text = data["question"]

        # Create FAQ
        next_order = await faq_service.get_next_order()
        await faq_service.create_faq(question_text, answer_text, next_order)

        # Clean up
        del self.adding_faq[user_id]

        await update.message.reply_text(
            f"✅ FAQ добавлен!\n\n❓ <b>{question_text}</b>\n📍 {answer_text}",
            parse_mode="HTML"
        )

        # Open FAQ edit menu
        await self.faq_edit_button_handler(update, context)
        return True

    async def faq_edit_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle edit FAQ callback"""
        query = update.callback_query
        await query.answer()

        user_id = query.from_user.id

        if not Config.is_admin(user_id):
            await query.edit_message_text("⛔ У вас нет прав.")
            return

        # Parse: faq_edit_{faq_id}
        data = query.data
        faq_id = int(data.split("_")[2])

        # Check if FAQ is being edited by another admin
        if faq_id in self.faq_locks and self.faq_locks[faq_id] != user_id:
            await query.edit_message_text(
                "⛔ Этот FAQ сейчас редактирует другой администратор. Попробуйте позже."
            )
            return

        faq = await faq_service.get_faq_by_id(faq_id)

        if not faq:
            await query.edit_message_text("❌ FAQ не найден.")
            return

        # Set lock
        self.faq_locks[faq_id] = user_id
        self.editing_faq[user_id] = {"step": "question", "faq_id": faq_id}

        message = f"""✏️ <b>Редактирование FAQ #{faq_id}</b>

❓ <b>Текущий вопрос:</b>
{faq.question}

📍 <b>Текущий ответ:</b>
{faq.answer}

Введите новый вопрос (или отправьте /skip чтобы оставить без изменения):"""

        await query.edit_message_text(message, parse_mode="HTML")

    async def faq_edit_receive_question(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Receive new question for FAQ"""
        user_id = update.effective_user.id

        if user_id not in self.editing_faq:
            return False

        data = self.editing_faq[user_id]
        if data.get("step") != "question":
            return False

        faq_id = data["faq_id"]
        faq = await faq_service.get_faq_by_id(faq_id)

        if not faq:
            # Release lock
            if faq_id in self.faq_locks:
                del self.faq_locks[faq_id]
            del self.editing_faq[user_id]
            await update.message.reply_text("❌ FAQ не найден.")
            return True

        question_text = update.message.text

        if question_text == "/skip":
            question_text = faq.question

        # Move to answer step
        self.editing_faq[user_id]["step"] = "answer"
        self.editing_faq[user_id]["new_question"] = question_text

        await update.message.reply_text(
            f"❓ Новый вопрос: <b>{question_text}</b>\n\nВведите новый ответ (или /skip чтобы оставить без изменения):",
            parse_mode="HTML"
        )
        return True

    async def faq_edit_receive_answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Receive new answer for FAQ"""
        user_id = update.effective_user.id

        if user_id not in self.editing_faq:
            return False

        data = self.editing_faq[user_id]
        if data.get("step") != "answer":
            return False

        faq_id = data["faq_id"]
        new_question = data.get("new_question")

        faq = await faq_service.get_faq_by_id(faq_id)

        if not faq:
            # Release lock
            if faq_id in self.faq_locks:
                del self.faq_locks[faq_id]
            del self.editing_faq[user_id]
            await update.message.reply_text("❌ FAQ не найден.")
            return True

        answer_text = update.message.text

        if answer_text == "/skip":
            answer_text = faq.answer

        if not new_question:
            new_question = faq.question

        # Update FAQ
        await faq_service.update_faq(faq_id, new_question, answer_text)

        # Release lock
        if faq_id in self.faq_locks:
            del self.faq_locks[faq_id]

        # Clean up
        del self.editing_faq[user_id]

        await update.message.reply_text(
            f"✅ FAQ обновлён!\n\n❓ <b>{new_question}</b>\n📍 {answer_text}",
            parse_mode="HTML"
        )
        return True

    async def faq_delete_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle delete FAQ callback"""
        query = update.callback_query
        await query.answer()

        user_id = query.from_user.id

        if not Config.is_admin(user_id):
            await query.edit_message_text("⛔ У вас нет прав.")
            return

        # Parse: faq_delete_{faq_id}
        data = query.data
        faq_id = int(data.split("_")[2])

        faq = await faq_service.get_faq_by_id(faq_id)

        if not faq:
            await query.edit_message_text("❌ FAQ не найден.")
            return

        # Delete FAQ
        await faq_service.delete_faq(faq_id)

        # Show updated FAQ list
        await self.faq_list_callback(update, context)

    async def faq_back_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle back button callback - return to FAQ edit menu"""
        query = update.callback_query
        await query.answer()

        user_id = query.from_user.id

        if not Config.is_admin(user_id):
            await query.edit_message_text("⛔ У вас нет прав.")
            return

        # Show FAQ edit menu
        faqs = await faq_service.get_all_faqs()

        if not faqs:
            message = """📝 <b>Редактирование FAQ</b>

Список пуст. Нажмите \"➕ Добавить\" чтобы создать первый вопрос."""
            keyboard = get_faq_management_keyboard(empty=True)
        else:
            message = f"""📝 <b>Редактирование FAQ</b>

Всего вопросов: {len(faqs)}

Выберите действие:"""
            keyboard = get_faq_management_keyboard(empty=False)

        await query.edit_message_text(
            message,
            parse_mode="HTML",
            reply_markup=keyboard
        )

    async def faq_exit_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle exit from FAQ menu - return to admin menu"""
        query = update.callback_query
        await query.answer()

        user_id = query.from_user.id

        if not Config.is_admin(user_id):
            await query.message.reply_text("⛔ У вас нет прав.")
            return

        from utils.keyboards import get_admin_menu_keyboard

        await query.message.reply_text(
            "🔙 Вы вернулись в админ-меню.",
            reply_markup=get_admin_menu_keyboard()
        )

    def clear_user_locks(self, user_id: int):
        """Clear all locks for a specific user (useful for cancel operations)"""
        if user_id in self.editing_faq:
            faq_id = self.editing_faq[user_id].get("faq_id")
            if faq_id and faq_id in self.faq_locks:
                del self.faq_locks[faq_id]
            del self.editing_faq[user_id]


admin_faq_handler = AdminFAQHandler()
