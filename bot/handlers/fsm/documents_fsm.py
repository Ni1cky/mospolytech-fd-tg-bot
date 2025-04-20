import datetime
from typing import Any, Dict

import pymorphy3

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    Message,
    CallbackQuery,
    InputMediaDocument,
    FSInputFile
)
from docxtpl import DocxTemplate

from bot.handlers.keyboards import inline_agreement_keyboard

documents_fsm_router = Router()


class ApplicationForm(StatesGroup):
    group_number = State()
    agreement = State()
    program_name = State()
    full_name = State()
    phone = State()
    current_date = State()
    email = State()


def cap_current_date():
    return '.'.join(reversed((str(datetime.date.today()).split('-'))))

@documents_fsm_router.message(F.text == "📄 Заполнить заявление")
@documents_fsm_router.message(Command("documents"))
async def start_filling_documents(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Начинаем заполнять данные:\n Потребуется ввести:\n"
        "* Фио\n"
        "* Номер телефона\n"
        "* Email\n"
        "* Номер группы\n"
        "При заполнении всех пунктов, мы пришлем тебе заявление, которое останется только подписать."
        "\nПродолжим?",
        reply_markup=inline_agreement_keyboard()
    )
    await state.set_state(ApplicationForm.agreement)


@documents_fsm_router.callback_query(F.data == "stop", ApplicationForm.agreement)
async def stop(call: CallbackQuery, state: FSMContext):
    await call.answer("Заполнение отменено")
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Чтобы начать заново: /documents")
    await state.clear()


def qualification_from_program(program_name: str):
    # TODO: Some logic of getting qualification name from program name
    return "Лучший специалист в мире"


def create_documents(data: Dict[str, Any]) -> list[InputMediaDocument]:
    result = []

    data["date"] = cap_current_date()
    data["full_name_gent"] = genter(data["full_name"])
    data["qualification_name"] = qualification_from_program(data["program_name"])

    statement = DocxTemplate("docs_templates/statement_template.docx")
    statement.render(data)
    file_path = f"created_docs/Statement {data['full_name']} {datetime.datetime.now().strftime('%d.%m.%Y-%H.%M.%S')}.docx"
    statement.save(file_path)

    statement_to_return = InputMediaDocument(media=FSInputFile(file_path))
    result.append(statement_to_return)

    return result


@documents_fsm_router.callback_query(F.data == "continue", ApplicationForm.agreement)
async def claim_agreement(call: CallbackQuery, state: FSMContext):
    await call.answer("Отправить")
    await call.message.edit_reply_markup(reply_markup=None)

    data = await state.get_data()
    if data.get("agreement"):
        await call.message.answer("Присылаем готовый документ. Подпиши его и отнеси в отдел МФЦ любого корпуса!")
        await call.message.answer_media_group(create_documents(data))
        await state.clear()
        return

    await call.message.answer("Ниже представлен список дисциплин, доступных для записи.\n"
                              "Выберите необходимую. (Пока ручной ввод).")  # ЗДЕСЬ НАДО БУДЕТ
    # ПОМЕНЯТЬ, ДЛЯ РЕАЛИЗАЦИИ КНОПКАМИ
    await state.update_data(agreement=True)
    await state.set_state(ApplicationForm.program_name)


@documents_fsm_router.message(F.text, ApplicationForm.program_name)
async def capture_program_name(message: Message, state: FSMContext):
    await state.update_data(program_name=message.text)
    await message.answer("ФИО:\n"
                         "(Иванов Иван Иванович)")
    await state.set_state(ApplicationForm.full_name)


def genter(word: str):
    morph = pymorphy3.MorphAnalyzer()
    results = []
    for part in word.split():
        result = morph.parse(part)[0].inflect({"gent"}).word
        results.append(result)
    return results


@documents_fsm_router.message(F.text, ApplicationForm.full_name)
async def capture_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Номер телефона:\n"
                         "(89269997799)")
    await state.set_state(ApplicationForm.phone)


def format_phone_number(phone_number: str):
    digits = "".join([digit for digit in phone_number if digit.isdigit()])
    formatted_number = f"+{digits[:-10]} ({digits[-10:-7]}) {digits[-7:-4]}-{digits[-4:-2]}-{digits[-2:]}"
    if formatted_number[1] == "8" and len(digits) == 11:
        formatted_number = "+7" + formatted_number[2:]
    return formatted_number


@documents_fsm_router.message(F.text, ApplicationForm.phone)
async def capture_phone(message: Message, state: FSMContext):
    await state.update_data(phone=format_phone_number(message.text))
    await message.answer("Email:\n"
                         "(abc@abc.abc)")
    await state.set_state(ApplicationForm.email)


@documents_fsm_router.message(F.text, ApplicationForm.email)
async def capture_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Номер группы:\n"
                         "(123-123)")
    await state.set_state(ApplicationForm.group_number)


@documents_fsm_router.message(F.text, ApplicationForm.group_number)
async def group_number(message: Message, state: FSMContext):
    await state.update_data(group_number=message.text)
    data = await state.get_data()
    await message.answer(
        f"Отлично, все данные введены!\n"
        f"Ты можешь проверить ниже правильность информации:\n\n"
        f"✓ Номер группы: {data['group_number']}\n"
        f"✓ Программа: {data['program_name']}\n"
        f"✓ ФИО: {data['full_name']}\n"
        f"✓ Номер телефона: {data['phone']}\n"
        f"✓ Email {data['email']}\n"
        f"Если все верно, нажимай Продолжить",
        reply_markup=inline_agreement_keyboard()
    )
    await state.set_state(ApplicationForm.agreement)
