from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from bot.handlers.keyboards import generate_faq_keyboard, back_to_faq_keyboard
from bot.handlers.faq_data import questions_and_answers


faq_router = Router()


@faq_router.message(F.text == "❓ FAQ")
@faq_router.message(Command("faq"))
async def faq_command_handler(message: Message) -> None:
    await message.answer(
        text="Выберите вопрос из списка, чтобы получить ответ:",
        reply_markup=generate_faq_keyboard()
    )


@faq_router.callback_query(F.data.startswith("faq_"))
async def answer_faq_callback(callback: CallbackQuery) -> None:
    try:
        index = int(callback.data.split("_")[1]) - 1
        if 0 <= index < len(questions_and_answers):
            question = list(questions_and_answers.keys())[index]
            answer = questions_and_answers[question]
            await callback.message.edit_text(
                text=f"<b>{question}</b>\n\n{answer}",
                reply_markup=back_to_faq_keyboard()
            )
    except (ValueError, IndexError):
        await callback.message.edit_text("Произошла ошибка. Попробуйте снова.")


@faq_router.callback_query(F.data == "back_to_faq")
async def back_to_faq_handler(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        text="Выберите вопрос из списка, чтобы получить ответ:",
        reply_markup=generate_faq_keyboard()
    )