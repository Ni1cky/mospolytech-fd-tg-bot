from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BotCommand

from bot.handlers.keyboards import after_start_keyboard



commands_router = Router()

ALL_COMMANDS = [
    BotCommand(command="start", description="Начать взаимодействие"),
    BotCommand(command="documents", description="Заполнить документы"),
    BotCommand(command="programs", description="Доступные программы"),
    BotCommand(command="advice", description="Подобрать программу"),
    BotCommand(command="cancel", description="Отменить"),
    BotCommand(command="faq", description="Часто задаваемые вопросы"),
]


@commands_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        text=
        "Выберите, что вам интересно узнать о программах дополнительного профессионального образования (ДПО):\n\n"
        "<b>🔹 Просмотр доступных программ</b>\n"
        "Узнайте о курсах и выберите подходящий для себя.\n\n"
        "<b>🔹 Рекомендации по выбору программы</b>\n"
        "Получите помощь в подборе курсов, которые будут полезны именно вам.\n\n"
        "<b>🔹 Заполнение заявления и договора</b>\n"
        "Заполните и получите готовые документы на обучение в формате Word.\n\n"
        "<b>🔹Ответы на часто задаваемые вопросы.</b>\n"
        "Получите ответы на ваши вопросы",
        reply_markup=after_start_keyboard()
    )


@commands_router.message(F.text == "❌ Отменить")
@commands_router.message(Command("cancel"))
async def cancel_command_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        text="Текущее действие было отменено. Вы вернулись на  главное меню.",
        reply_markup=after_start_keyboard()
    )


@commands_router.message(F.text.in_({"📊 Рекомендации", "📋 Просмотр программ"}))
@commands_router.message(Command("programs", "advice"))
async def not_implemented_commands_handler(message: Message) -> None:
    await message.answer("Пока не реализовано")
    # TODO: реализовать команду cancel. Она должна отменять любой текущий сценарий

