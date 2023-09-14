import logging
from aiogram import Bot, Dispatcher, types, executor

API_TOKEN = '6650827858:AAGgNXGMly3ox4qQFz0Ud5dZXcdF0TIJgPs'

user_id = "6420712889"

# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text="*** Привет, это бот 'Предложка 2107' *** \n\nЧтобы предложить новость отправь боту любое сообщение. Все сообщения полностью анонимны",
                           parse_mode="Markdown")


@dp.message_handler(commands=['help'])
async def on_start(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text="*** Внимание !!! *** \n\nБот в стадии тестировки и исправления ошибок, так что если вы обнаружили проблему, напишите сюда: \n\n@setta1a",
                           parse_mode="Markdown")


@dp.message_handler(content_types=["text", "photo", "video"])
async def check_messages(message: types.Message):
    if message.text:
        await bot.send_message(user_id,
                               "📨 *** Получено новое сообщение *** \n\n" + message.text,
                               parse_mode="Markdown")
    if message.photo:
        if message.caption:
            await bot.send_photo(user_id,
                                 message.photo[-1].file_id,
                                 caption="📨 *** Получено новое сообщение *** \n\n" + message.caption,
                                 parse_mode="Markdown")
        else:
            await bot.send_photo(user_id,
                                 message.photo[-1].file_id)
    if message.video:
        if message.caption:
            await bot.send_video(user_id,
                                 message.video.file_id,
                                 caption="📨 *** Получено новое сообщение *** \n\n" + message.caption,
                                 parse_mode="Markdown")
        else:
            await bot.send_video(user_id,
                                 message.video.file_id)

    await bot.send_message(message.chat.id, text="*** Ваше сообщение отправлено ***", parse_mode="Markdown")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
