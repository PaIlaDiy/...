import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import random

# Устанавливаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Список URL-адресов мотивационных картинок
motivation_pics = [
    'https://i.imgur.com/M6d44z4.png',
    'https://i.imgur.com/73kouUG.jpeg',
    'https://i.imgur.com/TpiENBe.jpeg',
    'https://i.imgur.com/L0lz0Uh.jpeg',
    'https://i.imgur.com/CouHtXx.jpeg',
    'https://i.imgur.com/BiCLs9E.jpeg',
    'https://i.imgur.com/5244qVX.png'
]

# Словарь для хранения идентификаторов последних сообщений с изображениями и последнего индекса картинки
last_image_data = {}


# Функция, которая будет вызываться при старте бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Получить мотивацию!", callback_data='get_motivation')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привет! Нажми на кнопку ниже, чтобы получить дозу мотивации.',
                                    reply_markup=reply_markup)


# Функция обработки нажатия на кнопку
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id

    # Удаляем предыдущее изображение, если оно существует
    if chat_id in last_image_data:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=last_image_data[chat_id]['message_id'])
        except Exception as e:
            logger.error(f"Ошибка при удалении сообщения: {e}")

    if query.data == 'get_motivation':
        last_index = last_image_data.get(chat_id, {}).get('last_index', -1)

        # Выбираем новую картинку, не совпадающую с последней отправленной
        new_index = last_index
        while new_index == last_index:
            new_index = random.randint(0, len(motivation_pics) - 1)

        pic_url = motivation_pics[new_index]
        sent_message = await query.message.reply_photo(photo=pic_url)

        # Сохраняем идентификатор последнего сообщения с изображением и индекс картинки
        last_image_data[chat_id] = {'message_id': sent_message.message_id, 'last_index': new_index}


def main() -> None:
    # Вставьте сюда ваш токен
    token = '7419303008:AAHcqMF6OGgPn55qr0D1R7PzCo06kJxN2is'

    # Создаем Application
    application = Application.builder().token(token).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Запуск бота
    application.run_polling()


if __name__ == '__main__':
    main()