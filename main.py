import logging
import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackContext,
)
from phone_api import get_phone_info  # Импорт модуля для проверки номеров

from dotenv import load_dotenv
load_dotenv()

# Настройка логов
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния диалога
(
    MAIN_MENU,
    TABLE_NAME_AGE,
    TABLE_NATION,
    TABLE_JOB,
    TABLE_PLACE_TIME,
    TABLE_PHONE,
    TABLE_EXTRA,
    GIRL_NAME_AGE,
    GIRL_NATION,
    GIRL_JOB,
    PHONE_INPUT
) = range(11)

# Клавиатуры
main_menu_markup = ReplyKeyboardMarkup(
    [["📝 Обычная анкета", "🛠 Чат поддержки", "🔍 Мини запрос"]],
    resize_keyboard=True,
    one_time_keyboard=True
)


# ================== ОСНОВНЫЕ ОБРАБОТЧИКИ ================== #
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Привет, друг! Я бот для создания анкет 🌟\nВыбери действие:",
        reply_markup=main_menu_markup
    )
    return MAIN_MENU


async def main_menu(update: Update, context: CallbackContext) -> int:
    choice = update.message.text

    if choice == "📝 Обычная анкета":
        await update.message.reply_text(
            "Отлично! Давай заполним анкету 🌟\n1) Имя и возраст стола:",
            reply_markup=ReplyKeyboardRemove()
        )
        return TABLE_NAME_AGE

    elif choice == "🛠 Чат поддержки":
        await update.message.reply_text(
            "📞 По всем вопросам пиши: @gooooodyyyy",
            reply_markup=main_menu_markup
        )
        return MAIN_MENU

    elif choice == "🔍 Мини запрос":
        await update.message.reply_text(
            "Введите номер в международном формате:\nПример: +79123456789",
            reply_markup=ReplyKeyboardRemove()
        )
        return PHONE_INPUT

    else:
        await update.message.reply_text("Используй кнопки меню 👇", reply_markup=main_menu_markup)
        return MAIN_MENU


# ================== ОБРАБОТЧИКИ АНКЕТЫ ================== #
async def table_name_age(update: Update, context: CallbackContext) -> int:
    context.user_data["table_name_age"] = update.message.text
    await update.message.reply_text("2) Нация стола:")
    return TABLE_NATION


async def table_nation(update: Update, context: CallbackContext) -> int:
    context.user_data["table_nation"] = update.message.text
    await update.message.reply_text("3) Профессия:")
    return TABLE_JOB


async def table_job(update: Update, context: CallbackContext) -> int:
    context.user_data["table_job"] = update.message.text
    await update.message.reply_text("4) Место и время встречи:")
    return TABLE_PLACE_TIME


async def table_place_time(update: Update, context: CallbackContext) -> int:
    context.user_data["table_place_time"] = update.message.text
    await update.message.reply_text("5) Номер телефона:")
    return TABLE_PHONE


async def table_phone(update: Update, context: CallbackContext) -> int:
    context.user_data["table_phone"] = update.message.text
    await update.message.reply_text("6) Доп. информация о столе и прогрев:")
    return TABLE_EXTRA


async def table_extra(update: Update, context: CallbackContext) -> int:
    context.user_data["table_extra"] = update.message.text
    await update.message.reply_text("Теперь информация о девушке:\n1) Ее имя и возраст:")
    return GIRL_NAME_AGE


async def girl_name_age(update: Update, context: CallbackContext) -> int:
    context.user_data["girl_name_age"] = update.message.text
    await update.message.reply_text("2) Нация девушки:")
    return GIRL_NATION


async def girl_nation(update: Update, context: CallbackContext) -> int:
    context.user_data["girl_nation"] = update.message.text
    await update.message.reply_text("3) Работа девушки:")
    return GIRL_JOB


async def girl_job(update: Update, context: CallbackContext) -> int:
    context.user_data["girl_job"] = update.message.text

    result = (
        "✅ Анкета готова:\n\n"
        "🧑 Информация о столе:\n"
        f"1) {context.user_data['table_name_age']}\n"
        f"2) {context.user_data['table_nation']}\n"
        f"3) {context.user_data['table_job']}\n"
        f"4) {context.user_data['table_place_time']}\n"
        f"5) {context.user_data['table_phone']}\n"
        f"6) {context.user_data['table_extra']}\n\n"
        "👩 Информация о девушке:\n"
        f"1) {context.user_data['girl_name_age']}\n"
        f"2) {context.user_data['girl_nation']}\n"
        f"3) {context.user_data['girl_job']}"
    )

    await update.message.reply_text(result, reply_markup=main_menu_markup)
    return ConversationHandler.END


# ================== ОБРАБОТЧИК ЗАПРОСА НОМЕРА ================== #
async def phone_input(update: Update, context: CallbackContext) -> int:
    phone = update.message.text
    info = get_phone_info(phone)

    if 'error' in info:
        response = f"❌ Ошибка: {info['error']}"
    elif not info.get('valid', False):
        response = "⚠️ Номер недействителен или не найден"
    else:
        response = (
            "📱 Результат проверки:\n"
            f"• Номер: {info.get('number', 'Н/Д')}\n"
            f"• Страна: {info.get('country', 'Н/Д')}\n"
            f"• Оператор: {info.get('operator', 'Н/Д')}\n"
            f"• Тип: {info.get('type', 'Н/Д')}"
        )

    await update.message.reply_text(response, reply_markup=main_menu_markup)
    return MAIN_MENU


# ================== СЛУЖЕБНЫЕ ФУНКЦИИ ================== #
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "❌ Диалог прерван. Возвращаюсь в меню",
        reply_markup=main_menu_markup
    )
    return MAIN_MENU


async def error_handler(update: Update, context: CallbackContext) -> None:
    logger.error(f"Ошибка: {context.error}")
    await update.message.reply_text("⚠️ Произошла ошибка. Используй /start")


# ================== ЗАПУСК ПРИЛОЖЕНИЯ ================== #
def main() -> None:
    application = ApplicationBuilder().token(os.getenv("8145461036:AAG1GH5SeLq_Dl_cqgJDf1WqaSj3o4ceaSs")).build()

    # Настройка обработчиков
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu)],
            TABLE_NAME_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, table_name_age)],
            TABLE_NATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, table_nation)],
            TABLE_JOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, table_job)],
            TABLE_PLACE_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, table_place_time)],
            TABLE_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, table_phone)],
            TABLE_EXTRA: [MessageHandler(filters.TEXT & ~filters.COMMAND, table_extra)],
            GIRL_NAME_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, girl_name_age)],
            GIRL_NATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, girl_nation)],
            GIRL_JOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, girl_job)],
            PHONE_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone_input)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_error_handler(error_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
