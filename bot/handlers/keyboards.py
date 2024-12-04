from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from bot.handlers.faq_data import questions_and_answers

def agreement_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Продолжить", callback_data="continue")],
        [InlineKeyboardButton(text="Стоп", callback_data="stop")]
    ])
    return keyboard


def after_start_keyboard():
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="📄 Заявление и договор")],
            [KeyboardButton(text="📋 Просмотр программ")],
            [KeyboardButton(text="📊 Рекомендации")],
            [KeyboardButton(text="❓ FAQ")],
            [KeyboardButton(text="❌ Отменить")],
        ])
    return keyboard

def generate_faq_keyboard():
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

def back_to_faq_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Вернуться к списку", callback_data="back_to_faq")]
        ]
    )
