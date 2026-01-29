from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from config import Config


def get_main_menu_keyboard():
    """Get main menu keyboard for regular users"""
    keyboard = [
        [KeyboardButton(Config.GUEST_QUESTION_BUTTON_TEXT)],
        [KeyboardButton(Config.FAQ_BUTTON_TEXT)]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_admin_menu_keyboard():
    """Get admin menu keyboard for admins"""
    keyboard = [
        [KeyboardButton(Config.ADMIN_GUESTS_BUTTON_TEXT), KeyboardButton(Config.ADMIN_STATS_BUTTON_TEXT)],
        [KeyboardButton(Config.ADMIN_EDIT_FAQ_BUTTON_TEXT), KeyboardButton(Config.FAQ_BUTTON_TEXT)]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_answer_keyboard(question_id: int, from_user_id: int) -> InlineKeyboardMarkup:
    """Get keyboard for answering a question"""
    keyboard = [
        [InlineKeyboardButton(
            "Ответить",
            callback_data=f"answer_{question_id}_{from_user_id}"
        )]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_faq_management_keyboard(empty: bool = False) -> InlineKeyboardMarkup:
    """Get FAQ management keyboard"""
    if empty:
        keyboard = [
            [InlineKeyboardButton("➕ Добавить", callback_data="faq_add")],
            [InlineKeyboardButton("◀️ Назад", callback_data="faq_exit")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("📋 Список", callback_data="faq_list")],
            [InlineKeyboardButton("➕ Добавить", callback_data="faq_add")],
            [InlineKeyboardButton("◀️ Назад", callback_data="faq_exit")]
        ]
    return InlineKeyboardMarkup(keyboard)


def get_faq_list_keyboard(faqs) -> InlineKeyboardMarkup:
    """Get FAQ list keyboard with edit/delete buttons"""
    keyboard = []
    for faq in faqs:
        # Shorten question for button
        short_question = faq.question[:20] + "..." if len(faq.question) > 20 else faq.question
        keyboard.append([
            InlineKeyboardButton(f"✏️ {short_question}", callback_data=f"faq_edit_{faq.id}"),
            InlineKeyboardButton("🗑", callback_data=f"faq_delete_{faq.id}")
        ])
    keyboard.append([InlineKeyboardButton("➕ Добавить", callback_data="faq_add")])
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="faq_back")])
    return InlineKeyboardMarkup(keyboard)
