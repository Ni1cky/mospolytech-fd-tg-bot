from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from bot.handlers.faq_data import questions_and_answers


def inline_agreement_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Продолжить", callback_data="continue")],
        [InlineKeyboardButton(text="Стоп", callback_data="stop")]
    ])
    return keyboard


def reply_after_start_keyboard():
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="📄 Заполнить заявление")],
            [KeyboardButton(text="📋 Просмотр дисциплин")],
            [KeyboardButton(text="❓ FAQ")],
            [KeyboardButton(text="❌ Отменить")],
        ])
    return keyboard


def inline_faq_keyboard():
    keyboard = []
    row = []
    for index, question in enumerate(questions_and_answers.keys(), start=1):
        row.append(
            InlineKeyboardButton(
                text=f"{index}",
                callback_data=f"faq_{index}"
            )
        )
        if len(row) == 5:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def inline_back_to_faq_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Вернуться к списку", callback_data="back_to_faq")]
        ]
    )
