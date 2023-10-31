import logging
import os
import random

from typing import List

from aiogram.dispatcher.filters import MediaGroupFilter
from aiogram.types import ContentType
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram_media_group import media_group_handler
from path_to_blacklist import path

from aiogram import Bot, Dispatcher, types, executor

API_TOKEN = '6650827858:AAGgNXGMly3ox4qQFz0Ud5dZXcdF0TIJgPs'

admin_id = "6420712889"

# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

is_raffle_start = False
raffle_members = []
print(os.getcwd())

@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    print("dasdsadasda:" + os.getcwd())
    await bot.send_message(chat_id=message.chat.id,
                           text="*** Привет, это бот 'Предложка 2107' *** \n\nЧтобы предложить новость отправь боту любое сообщение. Все сообщения полностью анонимны",
                           parse_mode="Markdown")


@dp.message_handler(commands=['help'])
async def on_help(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text="*** Внимание !!! *** \n\nБот в стадии тестировки и исправления ошибок, так что если вы обнаружили проблему, напишите сюда: \n\n@setta1a",
                           parse_mode="Markdown")


@dp.message_handler(commands=['raffle'])
async def on_raffle(message: types.Message):
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


@dp.message_handler(MediaGroupFilter(is_media_group=True), content_types=[ContentType.AUDIO, ContentType.PHOTO, ContentType.VIDEO, ContentType.TEXT])
@media_group_handler
async def album_handler(message: List[types.Message]):
    # reply keyboard -> ban user
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Забанить", callback_data=message[0]['from'].id)
    markup.add(button1)
    # create media list -> send to admin
    media = []
    for m in message:
        if m.photo:
            caption = ""
            if type(m.caption) == str:
                caption = "📨 *** Получено новое сообщение *** \n\n" + m.caption
            media.append(types.InputMediaPhoto(
                media=m.photo[-1].file_id,
                caption=caption,
                caption_entities=m.caption_entities,
                parse_mode="Markdown"
            ))
        elif m.video:
            caption = ""
            if type(m.caption) == str:
                caption = "📨 *** Получено новое сообщение *** \n\n" + m.caption
            media.append(types.InputMediaVideo(
                media=m.video.file_id,
                caption=caption,
                caption_entities=m.caption_entities,
                parse_mode="Markdown"
            ))
    # send messages separately (no keyboard + media_group)
    await bot.send_media_group(chat_id=admin_id, media=media)
    # with keyboard
    await bot.send_message(admin_id,
                           "Забанить?",
                           parse_mode="Markdown",
                           reply_markup=markup)


@dp.message_handler(content_types=["text", "photo", "video"])
async def check_messages(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    chat_id = message["from"].id
    banlist = open(path).readlines()
    if str(message["from"].id) + '\n' not in banlist:
        if message.text:
            button1 = types.InlineKeyboardButton("Забанить", callback_data=chat_id)
            markup.add(button1)
            await bot.send_message(admin_id,
                                   "📨 *** Получено новое сообщение *** \n\n" + message.text,
                                   parse_mode="Markdown",
                                   reply_markup=markup)
        if message.photo:
            print(message.photo)
            button1 = types.InlineKeyboardButton("Забанить", callback_data=chat_id)
            markup.add(button1)
            if message.caption:
                await bot.send_photo(admin_id,
                                     message.photo[-1].file_id,
                                     caption="📨 *** Получено новое сообщение *** \n\n" + message.caption,
                                     parse_mode="Markdown",
                                     reply_markup=markup)
            else:
                await bot.send_photo(admin_id,
                                     message.photo[-1].file_id,
                                     caption="📨 *** Получено новое фото *** \n",
                                     parse_mode="Markdown",
                                     reply_markup=markup)
        if message.video:
            print(message.video)
            button1 = types.InlineKeyboardButton("Забанить", callback_data=chat_id)
            markup.add(button1)
            if message.caption:
                await bot.send_video(admin_id,
                                     message.video.file_id,
                                     caption="📨 *** Получено новое сообщение *** \n\n" + message.caption,
                                     parse_mode="Markdown",
                                     reply_markup=markup)
            else:
                await bot.send_video(admin_id,
                                     message.video.file_id,
                                     caption="📨 *** Получено новое видео *** \n",
                                     parse_mode="Markdown",
                                     reply_markup=markup)

        await bot.send_message(message.chat.id, text="*** Ваше сообщение отправлено ***", parse_mode="Markdown")
    else:
        await bot.send_message(message.chat.id, text="*** Вы находитесь в чёрном списке данного бота ***"
                                                     "\n\nЕсли вы считаете, что попали сюда незаслуженно, напишите администратору данного бота\n\n@setta1a", parse_mode="Markdown")


@dp.callback_query_handler(lambda call: str)
async def ban_user(call):
    print(os.getcwd())
    file = open(path, "a")
    file.write(str(call.data) + '\n')
    file.close()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
