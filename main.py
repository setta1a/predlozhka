import logging
from aiogram import Bot, Dispatcher, types, executor

API_TOKEN = '5805471744:AAGRKUJld2uqDC1N45C4OtpSzjUBhUl1LYs'

admin_id = "6420712889"

# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

def get_blacklist():
    blacklist = open("blacklist.txt").readlines()
    for i in range(len(blacklist)):
        blacklist[i] = blacklist[i].replace("\n", "")

    return blacklist


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


@dp.message_handler(commands=['blacklist'])
async def on_start(message: types.Message):
    print(message.chat.id, admin_id)
    if int(message.chat.id) == int(admin_id):
        text = message.text.replace("/blacklist", "").strip()

        if not text:
            blacklist = open("blacklist.txt")
            mess = ""
            for user in blacklist.readlines():
                mess += user
            await bot.send_message(admin_id, text="Черный писок:  \n" + mess)
            blacklist.close()

        else:
            blacklist = open("blacklist.txt", "a")
            blacklist.write(text + "\n")
            blacklist.close()

    else:
        await bot.send_message(message.chat.id, text="Вы не являетесь администратором данного бота.")


@dp.message_handler(content_types=["text", "photo", "video"])
async def check_messages(message: types.Message):
    if "@" + message["from"].username not in get_blacklist():
        if message.text:
            await bot.send_message(admin_id,
                                   "📨 *** Получено новое сообщение *** \n\n" + message.text,
                                   parse_mode="Markdown")
        if message.photo:
            if message.caption:
                await bot.send_photo(admin_id,
                                     message.photo[-1].file_id,
                                     caption="📨 *** Получено новое сообщение *** \n\n" + message.caption,
                                     parse_mode="Markdown")
            else:
                await bot.send_photo(admin_id,
                                     message.photo[-1].file_id)
        if message.video:
            if message.caption:
                await bot.send_video(admin_id,
                                     message.video.file_id,
                                     caption="📨 *** Получено новое сообщение *** \n\n" + message.caption,
                                     parse_mode="Markdown")
            else:
                await bot.send_video(admin_id,
                                     message.video.file_id)

        await bot.send_message(message.chat.id, text="*** Ваше сообщение отправлено ***", parse_mode="Markdown")
    else:
        await bot.send_message(message.chat.id, text="*** Вы в черном списке ***", parse_mode="Markdown")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
