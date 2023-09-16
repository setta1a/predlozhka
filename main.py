import logging
import random

from aiogram import Bot, Dispatcher, types, executor

API_TOKEN = '6650827858:AAGgNXGMly3ox4qQFz0Ud5dZXcdF0TIJgPs'

admin_id = "6420712889"

# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

is_raffle_start = False
raffle_members = []


def get_blacklist():
    blacklist = open("blacklist.txt ").readlines()
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


@dp.message_handler(commands=['raffle'])
async def on_start(message: types.Message):
    text = message.text.replace("/raffle", "").strip()
    global is_raffle_start
    global raffle_members
    if text == "start":
        raffle_members = []
        if message.chat.id != int(admin_id):
            await bot.send_message(chat_id=message.chat.id,
                                   text="*** Вы не являетесь администратором данного бота ***",
                                   parse_mode="Markdown")
        else:
            is_raffle_start = True
    elif text == "end":
        if message.chat.id != int(admin_id):
            await bot.send_message(chat_id=message.chat.id,
                                   text="*** Вы не являетесь администратором данного бота ***",
                                   parse_mode="Markdown")
        else:
            is_raffle_start = False
    elif text == "results":
        if message.chat.id != int(admin_id):
            await bot.send_message(chat_id=message.chat.id,
                                   text="*** Вы не являетесь администратором данного бота ***",
                                   parse_mode="Markdown")
        else:
            winner = random.choice(
                                       raffle_members)
            await bot.send_message(chat_id=admin_id,
                                   text="*** Победитель розыгрыша: *** \n\nhttps://web.telegram.org/k/#" + str(winner),
                                   parse_mode="Markdown")
            await bot.send_message(chat_id=winner,
                                   text="*** Ты выиграл(а) в розыгрыше!!! ***",
                                   parse_mode="Markdown")

    elif not text:
        if is_raffle_start:
            if message.chat.id not in raffle_members:
                raffle_members.append(message.chat.id)
                await bot.send_message(chat_id=message.chat.id,
                                       text="*** Вы приняли участие в розыгрыше ***",
                                       parse_mode="Markdown")
            else:
                await bot.send_message(chat_id=message.chat.id,
                                       text="*** Вы уже учавствуете в розыгрыше ***",
                                       parse_mode="Markdown")

        else:
            await bot.send_message(chat_id=message.chat.id,
                                   text="*** К сожалению, в данный момент не проходит ни одного розыгрыша ***",
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
            print(message.photo)
            if message.caption:
                await bot.send_photo(admin_id,
                                     message.photo[-1].file_id,
                                     caption="📨 *** Получено новое сообщение *** \n\n" + message.caption,
                                     parse_mode="Markdown")
            else:
                await bot.send_photo(admin_id,
                                     message.photo[-1].file_id,
                                     caption="📨 *** Получено новое фото *** \n",
                                     parse_mode="Markdown")
        if message.video:
            print(message.video)
            if message.caption:
                await bot.send_video(admin_id,
                                     message.video.file_id,
                                     caption="📨 *** Получено новое сообщение *** \n\n" + message.caption,
                                     parse_mode="Markdown")
            else:
                await bot.send_video(admin_id,
                                     message.video.file_id,
                                     caption="📨 *** Получено новое видео *** \n",
                                     parse_mode="Markdown")

        await bot.send_message(message.chat.id, text="*** Ваше сообщение отправлено ***", parse_mode="Markdown")
    else:
        await bot.send_message(message.chat.id, text="*** Вы в черном списке ***", parse_mode="Markdown")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
