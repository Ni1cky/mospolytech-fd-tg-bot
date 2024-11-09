from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)


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
            [KeyboardButton(text="ℹ️ FAQ")],
        ])
    return keyboard
