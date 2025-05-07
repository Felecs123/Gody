import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackContext,
)

# Настройка логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
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
) = range(10)

# Клавиатуры
main_menu_markup = ReplyKeyboardMarkup(
    [['📝 Обычная анкета', '🛠 Чат поддержки']],
    resize_keyboard=True,
    one_time_keyboard=True
)

# ================== Обработчики ================== #
async def start(update: Update, context: CallbackContext) -> int:
    """Начало работы, главное меню"""
    await update.message.reply_text(
        "Привет, друг! Я бот для создания анкет 🌟\nВыбери действие:",
        reply_markup=main_menu_markup
    )
    return MAIN_MENU

async def main_menu(update: Update, context: CallbackContext) -> int:
    """Обработка выбора в главном меню"""
    user_choice = update.message.text
    
    if user_choice == '📝 Обычная анкета':
        await update.message.reply_text(
            "Отлично! Давай заполним анкету 🌟\n1) Имя и возраст стола:",
            reply_markup=ReplyKeyboardRemove()
        )
        return TABLE_NAME_AGE
        
    elif user_choice == '🛠 Чат поддержки':
        await update.message.reply_text(
            "📞 По всем вопросам пиши: @gooooodyyyy",
            reply_markup=main_menu_markup
        )
        return MAIN_MENU
        
    else:
        await update.message.reply_text("Используй кнопки меню 👇", reply_markup=main_menu_markup)
        return MAIN_MENU

# ========== Обработчики анкеты ========== #
async def table_name_age(update: Update, context: CallbackContext) -> int:
    context.user_data['table_name_age'] = update.message.text
    await update.message.reply_text("2) Нация стола:")
    return TABLE_NATION

async def table_nation(update: Update, context: CallbackContext) -> int:
    context.user_data['table_nation'] = update.message.text
    await update.message.reply_text("3) Профессия:")
    return TABLE_JOB

async def table_job(update: Update, context: CallbackContext) -> int:
    context.user_data['table_job'] = update.message.text
    await update.message.reply_text("4) Место и время встречи:")
    return TABLE_PLACE_TIME

async def table_place_time(update: Update, context: CallbackContext) -> int:
    context.user_data['table_place_time'] = update.message.text
    await update.message.reply_text("5) Номер телефона:")
    return TABLE_PHONE

async def table_phone(update: Update, context: CallbackContext) -> int:
    context.user_data['table_phone'] = update.message.text
    await update.message.reply_text("6) Доп. информация о столе и прогрев:")
    return TABLE_EXTRA

async def table_extra(update: Update, context: CallbackContext) -> int:
    context.user_data['table_extra'] = update.message.text
    await update.message.reply_text("Теперь информация о девушке:\n1) Ее имя и возраст:")
    return GIRL_NAME_AGE

async def girl_name_age(update: Update, context: CallbackContext) -> int:
    context.user_data['girl_name_age'] = update.message.text
    await update.message.reply_text("2) Нация девушки:")
    return GIRL_NATION

async def girl_nation(update: Update, context: CallbackContext) -> int:
    context.user_data['girl_nation'] = update.message.text
    await update.message.reply_text("3) Работа девушки:")
    return GIRL_JOB

async def girl_job(update: Update, context: CallbackContext) -> int:
    context.user_data['girl_job'] = update.message.text
    
    # Формируем итоговую анкету
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

async def cancel(update: Update, context: CallbackContext) -> int:
    """Обработка команды /cancel"""
    await update.message.reply_text(
        "Диалог прерван. Возвращаюсь в главное меню 🏠",
        reply_markup=main_menu_markup
    )
    return MAIN_MENU

async def error_handler(update: Update, context: CallbackContext) -> None:
    """Логирование ошибок"""
    logger.error(f"Ошибка: {context.error}")
    await update.message.reply_text("⚠️ Произошла ошибка. Попробуйте /start")

# ================== Запуск ================== #
def main() -> None:
    application = ApplicationBuilder().token("8145461036:AAG1GH5SeLq_Dl_cqgJDf1WqaSj3o4ceaSs").build()

    # Добавляем обработчик обычных команд
    application.add_handler(CommandHandler("cancel", cancel))

    # Настройка ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
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
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)
    application.add_error_handler(error_handler)
    application.run_polling()

if __name__ == '__main__':
    main()
