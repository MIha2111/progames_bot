import logging

from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from games import games
from modes import modes

TOKEN = '6894683307:AAGCK0eynVTU8ZsXJ6CbZrnP82pmA6Wo_oY'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

async def set_deffault_commands(dp):
    await bot.set_my_commands(
        [
            types.BotCommand("start", "розпочати"),
            types.BotCommand("steam", "посилання на інші ігри"),       
            types.BotCommand("contacts", "контакти"),
            types.BotCommand("help", "список команд"),
            types.BotCommand("mode", "категоріі")
        ]
    )


@dp.message_handler(commands="start")
async def start(message: types.Message):
    game_choice = InlineKeyboardMarkup()
    for game in games:
        button = InlineKeyboardButton(text=game , callback_data=game)
        game_choice.add(button)
    await message.answer(text="Привіт, я бот який допоможе тобі скачати гру в Steam. Обери гру яку ти хочеш скачати" , reply_markup=game_choice)

@dp.message_handler(commands="steam")
async def steam(message: types.Message):
    message2 = "посилання на інші ігри: https://store.steampowered.com/"
    await message.answer(text=message2)

@dp.message_handler(commands="contacts")
async def contacts(message: types.Message):
    message3 = "пошта та номер для рекламодавців: mihamiron2111@gmail.com , 786345615" 
    await message.answer(text=message3)

@dp.message_handler(commands='help')
async def help(message: types.Message):
    help_text = (
        "Список команд:\n"
        "/start : Почати роботу з ботом\n"
        "/steam : Посилання на стім \n"
        "/contacts : Kонтакти \n"
        "/mode : Посилання на категорію гри" 
    )
    await message.answer(help_text)

@dp.message_handler(commands="mode")
async def modeww(message: types.Message):
    mode_choice = InlineKeyboardMarkup()
    for mode in modes:
        button1 = InlineKeyboardButton(text=mode, callback_data=mode)
        mode_choice.add(button1)
    await message.answer(text="Привіт, обери категорію гри", reply_markup=mode_choice)

    
@dp.callback_query_handler()
async def choice(callback_query: types.CallbackQuery):
    if callback_query.data in games.keys():
        await game(callback_query)
    elif callback_query.data in modes.keys():
        await mode(callback_query)

async def game(callback_query: types.CallbackQuery):
    await bot.send_photo(callback_query.message.chat.id, games[callback_query.data]["photo"])
    siteurl = games[callback_query.data]["siteurl"]
    about = games[callback_query.data]["about"]
    creator = games[callback_query.data]["creator"]
    price = games[callback_query.data]["price"]
    message = f"<b>Натисніть сюди щоб скачати: </b> {siteurl}\n\n<b>Про гру:</b> {about}\n<b>Tворець: </b> {creator}\n\n<b>Ціна: </b> {price}"
    await bot.send_message(callback_query.message.chat.id, message, parse_mode="html")

async def mode(callback_query: types.CallbackQuery):
    siteurl2 = modes[callback_query.data]
    message = f"<b>Натисніть сюди щоб перейти на сайт: </b> {siteurl2}"
    await bot.send_message(callback_query.message.chat.id, message, parse_mode="html")



async def on_startup(dp):
    await set_deffault_commands(dp)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)