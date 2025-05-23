import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from db import add_bot, get_all_bots
from handlers import register_handlers

import os

BOT_TOKEN_UTAMA = os.getenv("BOT_TOKEN_UTAMA")
bot_utama = Client("bot_utama", bot_token=BOT_TOKEN_UTAMA)

# Simple state management untuk menerima token bot baru
user_state = {}

@bot_utama.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Tambah Bot Token", callback_data="add_bot")],
        [InlineKeyboardButton("Daftar Bot", callback_data="list_bots")]
    ])
    await message.reply("Selamat datang di Bot Utama Anti-GCAST.\nPilih menu:", reply_markup=keyboard)

@bot_utama.on_callback_query()
async def callback_query_handler(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    if query.data == "add_bot":
        await query.message.edit("Silakan kirim token bot yang ingin ditambahkan.")
        user_state[user_id] = "await_token"
    elif query.data == "list_bots":
        bots = get_all_bots()
        if bots:
            text = "Daftar Bot:\n" + "\n".join([f"- @{b['bot_username']}" for b in bots])
        else:
            text = "Belum ada bot terdaftar."
        await query.message.edit(text)

@bot_utama.on_message(filters.private)
async def private_message_handler(client: Client, message: Message):
    user_id = message.from_user.id
    if user_state.get(user_id) == "await_token":
        token = message.text.strip()
        try:
            new_bot = Client(":memory:", bot_token=token)
            await new_bot.start()
            me = await new_bot.get_me()
            add_bot(token, me.id, me.username)
            await message.reply(f"Bot @{me.username} berhasil ditambahkan!")
            await new_bot.stop()
            user_state.pop(user_id)
        except Exception as e:
            await message.reply(f"Token tidak valid atau gagal terhubung.\nError: {e}")

async def start_all_bots():
    bots = get_all_bots()
    tasks = []
    for b in bots:
        app = Client(f"bot_{b['bot_id']}", bot_token=b["bot_token"])
        register_handlers(app)
        tasks.append(app.start())
    await asyncio.gather(*tasks)

async def stop_all_bots():
    bots = get_all_bots()
    tasks = []
    for b in bots:
        app = Client(f"bot_{b['bot_id']}", bot_token=b["bot_token"])
        tasks.append(app.stop())
    await asyncio.gather(*tasks)
