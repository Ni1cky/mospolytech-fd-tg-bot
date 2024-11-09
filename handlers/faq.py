from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from handlers.keyboards import after_start_keyboard

faq_router = Router()

FAQ_DATA = {
    "Что такое ДПО?": "ДПО (дополнительное профессиональное образование) — это программы для повышения квалификации и переподготовки специалистов, помогающие освоить новые навыки и знания.",
    "Какие программы предлагает Московский Политех?": "Московский Политех предлагает курсы по IT, менеджменту, маркетингу, инженерии и многим другим направлениям.",
    "Как записаться на курс?": "Вы можете оставить заявку прямо в этом боте или на сайте. Просто выберите программу, и мы свяжемся с вами для уточнения деталей.",
    "Какие документы нужны для записи?": "Для записи потребуются паспорт, СНИЛС и диплом об образовании. Для некоторых программ может потребоваться дополнительная информация.",
    "Как проходит обучение?": "Форматы: очный, дистанционный или смешанный, в зависимости от выбранной программы.",
    "Сколько длится курс?": "Курсы могут длиться от нескольких недель до нескольких месяцев, в зависимости от программы.",
    "Сколько стоит обучение?": "Стоимость зависит от программы. Подробнее на сайте ДПО или в боте.",
    "Можно ли получить льготы?": "Для студентов и выпускников Московского Политеха предусмотрены льготы и скидки. Уточните у сотрудника ДПО.",
    "Какой документ выдается после окончания курса?": "Вы получите удостоверение о повышении квалификации или диплом о переподготовке в зависимости от программы.",
    "Помогает ли университет с трудоустройством?": "Мы сотрудничаем с компаниями и предлагаем карьерные консультации для выпускников.",
    "Какие перспективы открывает программа?": "ДПО программы помогают перейти на более высокие должности, освоить новые навыки и повысить востребованность на рынке труда.",
    "Есть ли программы для иностранных студентов?": "Да, доступны курсы для международных студентов, в том числе и на английском языке.",
    "Как получить помощь при проблемах с платформой?": "Если возникли трудности с доступом или материалами, свяжитесь с нашей техподдержкой по контактам ниже или через кнопку Техподдержка.",
    "Контакт для вопросов и консультаций": "Телефон: +7(495) 223-05-23\nПочта: inopt@mospolytech.ru",
}

def get_faq_menu():
    keyboard = InlineKeyboardBuilder()
    for question in FAQ_DATA.keys():
        keyboard.button(text=question, callback_data=f"faq:{question}")

    keyboard.button(text="⬅️ Назад", callback_data="faq_back")
    keyboard.button(text="❌ Отмена", callback_data="faq_cancel")

    return keyboard.as_markup()

@faq_router.message(commands=["faq"])
async def faq_command(message: Message):
    keyboard = InlineKeyboardBuilder()
    for question in FAQ_DATA.keys():
        keyboard.button(text=question, callback_data=f"faq:{question}")

    await message.answer("Выберите интересующий вас вопрос:", reply_markup=keyboard.as_markup())


@faq_router.callback_query(lambda callback: callback.data.startswith("faq:"))
async def faq_answer(callback: CallbackQuery):
    question = callback.data.split("faq:")[1]
    answer = FAQ_DATA.get(question, "Извините, ответ на этот вопрос не найден.")

    await callback.message.answer(f"<b>{question}</b>\n\n{answer}")
    await callback.answer()

@faq_router.callback_query(lambda callback: callback.data == "faq_back")
async def faq_back(callback: CallbackQuery):
    await callback.message.answer("Вы вернулись в главное меню.", reply_markup=after_start_keyboard())
    await callback.answer()

@faq_router.callback_query(lambda callback: callback.data == "faq_cancel")
async def faq_cancel(callback: CallbackQuery):
    await callback.message.answer("Вы вышли из раздела FAQ.", reply_markup=after_start_keyboard())
    await callback.answer()