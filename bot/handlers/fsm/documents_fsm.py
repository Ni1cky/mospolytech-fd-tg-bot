from datetime import datetime
from typing import Any, Dict

import pymorphy3

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    Message,
    CallbackQuery,
    FSInputFile
)
from docxtpl import DocxTemplate

from bot.handlers.keyboards import inline_agreement_keyboard

documents_fsm_router = Router()


def genitive_case(name: str):
    """Родительный падеж имени"""
    morph = pymorphy3.MorphAnalyzer()
    results = []
    for part in name.split():
        result = morph.parse(part)[0].inflect({"gent"}).word
        results.append(result.capitalize() if part.istitle() else result)
    return results


def fill_statement_with_fsm_data(fsm_data: Dict[str, Any]) -> FSInputFile:
    fsm_data["today"] = datetime.now().strftime("%d.%m.%Y")
    # не используется внутри шаблона документа
    fsm_data["full_name_genitive"] = genitive_case(fsm_data["full_name"])

    statement = DocxTemplate("docs_templates/statement_template.docx")
    statement.render(fsm_data)
    file_path = f"created_docs/Statement {fsm_data['full_name']} {datetime.now().strftime('%d.%m.%Y-%H.%M.%S')}.docx"
    statement.save(file_path)

    return FSInputFile(file_path)


def format_phone_number(phone_number: str):
    digits = "".join([digit for digit in phone_number if digit.isdigit()])
    formatted_number = f"+{digits[:-10]} ({digits[-10:-7]}) {digits[-7:-4]}-{digits[-4:-2]}-{digits[-2:]}"
    if formatted_number[1] == "8" and len(digits) == 11:
        formatted_number = "+7" + formatted_number[2:]
    return formatted_number


class ApplicationForm(StatesGroup):
    full_name = State()
    phone = State()
    email = State()
    discipline_name = State()
    group_number = State()
    agreement = State()


@documents_fsm_router.message(F.text == "📄 Заполнить заявление")
@documents_fsm_router.message(Command("documents"))
async def start_filling_documents(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Начинаем заполнять данные, потребуется ввести:\n"
        "ФИО\n"
        "Номер телефона\n"
        "Email\n"
        "Номер учебной группы\n"
        "Название дисциплины для записи\n"
        "При заполнении всех пунктов мы пришлем тебе заявление, которое останется только подписать."
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


@documents_fsm_router.callback_query(F.data == "continue", ApplicationForm.agreement)
async def claim_agreement(call: CallbackQuery, state: FSMContext):
    await call.answer("Продолжаем")
    await call.message.edit_reply_markup(reply_markup=None)

    data = await state.get_data()
    if data.get("agreement"):
        await call.message.answer("Присылаем готовый документ. Подпиши его и отнеси в отдел МФЦ любого корпуса!")
        await call.message.answer_document(fill_statement_with_fsm_data(data))
        await state.clear()
        return

    await state.update_data(agreement=True)
    await call.message.answer("Теперь укажите номер Вашей учебной группы:\n(123-456)")
    await state.set_state(ApplicationForm.group_number)


@documents_fsm_router.message(F.text, ApplicationForm.group_number)
async def capture_group_number(message: Message, state: FSMContext):
    await state.update_data(group_number=message.text)
    # Todo здесь парсим сайт+документ и предлагаем на выбор дисциплины
    await message.answer(
        "Ниже представлен список дисциплин, доступных для записи.\nВыберите необходимую. (Пока ручной ввод)."
    )
    await state.set_state(ApplicationForm.discipline_name)


@documents_fsm_router.message(F.text, ApplicationForm.discipline_name)
async def capture_discipline_name(message: Message, state: FSMContext):
    await state.update_data(discipline_name=message.text)
    await message.answer("Укажите Ваше ФИО полностью:")
    await state.set_state(ApplicationForm.full_name)


@documents_fsm_router.message(F.text, ApplicationForm.full_name)
async def capture_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Укажите Ваш номер телефона:")
    await state.set_state(ApplicationForm.phone)


@documents_fsm_router.message(F.text, ApplicationForm.phone)
async def capture_phone(message: Message, state: FSMContext):
    await state.update_data(phone=format_phone_number(message.text))
    await message.answer("Укажите Ваш email:")
    await state.set_state(ApplicationForm.email)


@documents_fsm_router.message(F.text, ApplicationForm.email)
async def capture_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)

    data = await state.get_data()
    await message.answer(
        f"Отлично, все данные введены!\n"
        f"Ты можешь проверить правильность внесённых данных:\n\n"
        f"✓ Номер группы: {data['group_number']}\n"
        f"✓ Дисциплина: {data['discipline_name']}\n"
        f"✓ ФИО: {data['full_name']}\n"
        f"✓ Номер телефона: {data['phone']}\n"
        f"✓ Email {data['email']}\n"
        f"Если все верно, нажимай Продолжить",
        reply_markup=inline_agreement_keyboard()
    )
    await state.set_state(ApplicationForm.agreement)
