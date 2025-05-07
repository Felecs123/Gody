from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import logging

# Настройка логов
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Этапы разговора
(
    TABLE_INFO_START,
    TABLE_NAME_AGE,
    TABLE_NATION,
    TABLE_JOB,
    TABLE_PLACE_TIME,
    TABLE_PHONE,
    TABLE_EXTRA,
    GIRL_INFO_START,
    GIRL_NAME_AGE,
    GIRL_NATION,
    GIRL_JOB,
) = range(11)

# Клавиатура для отмены
reply_keyboard = [['/cancel']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

def start(update, context):
    user = update.message.from_user
    update.message.reply_text(
        f"Приветствую, друг! Я бот, разработанный чтобы помочь тебе быстрее делать анкеты для столов 🥰\n"
        "Ответь на следующие вопросы:\n\n"
        "1) Имя и возраст",
        reply_markup=markup
    )
    return TABLE_NAME_AGE

def table_name_age(update, context):
    context.user_data['table_name_age'] = update.message.text
    update.message.reply_text("2) Нация")
    return TABLE_NATION

def table_nation(update, context):
    context.user_data['table_nation'] = update.message.text
    update.message.reply_text("3) Профессия")
    return TABLE_JOB

def table_job(update, context):
    context.user_data['table_job'] = update.message.text
    update.message.reply_text("4) Место и время встречи")
    return TABLE_PLACE_TIME

def table_place_time(update, context):
    context.user_data['table_place_time'] = update.message.text
    update.message.reply_text("5) Номер:")
    return TABLE_PHONE

def table_phone(update, context):
    context.user_data['table_phone'] = update.message.text
    update.message.reply_text("6) Доп. инфа о столе и прогрев:")
    return TABLE_EXTRA

def table_extra(update, context):
    context.user_data['table_extra'] = update.message.text
    update.message.reply_text("Отлично 🥰 Ты заполнил инфу о столе, теперь перейдем к информации о девушке:\n\n1) Имя и возраст девушки")
    return GIRL_NAME_AGE

def girl_name_age(update, context):
    context.user_data['girl_name_age'] = update.message.text
    update.message.reply_text("2) Нация девушки")
    return GIRL_NATION

def girl_nation(update, context):
    context.user_data['girl_nation'] = update.message.text
    update.message.reply_text("3) Работа")
    return GIRL_JOB

def girl_job(update, context):
    context.user_data['girl_job'] = update.message.text
    # Формируем анкету
    table_info = (
        f"Информация о столе:\n"
        f"1) {context.user_data['table_name_age']}\n"
        f"2) {context.user_data['table_nation']}\n"
        f"3) {context.user_data['table_job']}\n"
        f"4) {context.user_data['table_place_time']}\n"
        f"5) {context.user_data['table_phone']}\n"
        f"6) {context.user_data['table_extra']}\n\n"
        f"Информация о ней:\n"
        f"1) {context.user_data['girl_name_age']}\n"
        f"2) {context.user_data['girl_nation']}\n"
        f"3) {context.user_data['girl_job']}"
    )
    update.message.reply_text(table_info, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text('Диалог прерван. Если бот не работает, напишите @ваш_логин')
    return ConversationHandler.END

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    update.message.reply_text('Ошибка. Если бот не работает, напишите @ваш_логин')

def main():
    updater = Updater("8145461036:AAG1GH5SeLq_Dl_cqgJDf1WqaSj3o4ceaSs", use_context=True) # Замените на свой токен
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            TABLE_NAME_AGE: [MessageHandler(Filters.text & ~Filters.command, table_name_age)],
            TABLE_NATION: [MessageHandler(Filters.text & ~Filters.command, table_nation)],
            TABLE_JOB: [MessageHandler(Filters.text & ~Filters.command, table_job)],
            TABLE_PLACE_TIME: [MessageHandler(Filters.text & ~Filters.command, table_place_time)],
            TABLE_PHONE: [MessageHandler(Filters.text & ~Filters.command, table_phone)],
            TABLE_EXTRA: [MessageHandler(Filters.text & ~Filters.command, table_extra)],
            GIRL_NAME_AGE: [MessageHandler(Filters.text & ~Filters.command, girl_name_age)],
            GIRL_NATION: [MessageHandler(Filters.text & ~Filters.command, girl_nation)],
            GIRL_JOB: [MessageHandler(Filters.text & ~Filters.command, girl_job)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()