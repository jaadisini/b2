from pyrogram import Client, filters
from pyrogram.types import Message
from db import (
    get_group_status, add_whitelist, remove_whitelist, list_whitelist,
    add_blacklist_user, remove_blacklist_user, list_blacklist_user,
    add_blacklist_trigger, remove_blacklist_trigger, list_blacklist_trigger,
    set_group_status
)

def is_gcast_message(text: str, triggers: list) -> bool:
    text = text.lower()
    for trig in triggers:
        if trig.lower() in text:
            return True
    return False

def register_handlers(app: Client):
    @app.on_message(filters.group)
    async def antigcast_filter(client: Client, message: Message):
        chat_id = message.chat.id
        user = message.from_user
        if not user:
            return
        user_id = user.id

        if not get_group_status(chat_id):
            return  # Anti-GCAST off

        whitelist = list_whitelist()
        if user_id in whitelist:
            return

        triggers = list_blacklist_trigger()
        if not message.text:
            return
        if is_gcast_message(message.text, triggers):
            blacklist_users = list_blacklist_user()
            if user_id in blacklist_users:
                try:
                    await message.delete()
                except:
                    pass

    @app.on_message(filters.command("ankes") & filters.group)
    async def cmd_ankes(client: Client, message: Message):
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in ("administrator", "creator"):
            await message.reply("Hanya admin yang dapat mengubah status anti-GCAST.")
            return
        args = message.text.split()
        if len(args) < 2 or args[1].lower() not in ("on", "off"):
            await message.reply("Gunakan: /ankes on atau /ankes off")
            return
        status = args[1].lower() == "on"
        set_group_status(message.chat.id, status)
        await message.reply(f"Anti-GCAST {'diaktifkan' if status else 'dinonaktifkan'} untuk grup ini.")

    @app.on_message(filters.command(["bl", "delbl", "wl", "unwl", "listwl", "dor", "undor", "listdor"]) & filters.group)
    async def manage_lists(client: Client, message: Message):
        cmd = message.text.split()[0][1:]
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in ("administrator", "creator"):
            await message.reply("Hanya admin yang dapat menggunakan perintah ini.")
            return
        args = message.text.split(maxsplit=1)

        if cmd == "bl":
            if len(args) < 2:
                await message.reply("Kirim perintah: /bl kata_trigger")
                return
            add_blacklist_trigger(args[1].strip())
            await message.reply(f"Trigger blacklist '{args[1]}' ditambahkan.")

        elif cmd == "delbl":
            if len(args) < 2:
                await message.reply("Kirim perintah: /delbl kata_trigger")
                return
            remove_blacklist_trigger(args[1].strip())
            await message.reply(f"Trigger blacklist '{args[1]}' dihapus.")

        elif cmd == "wl":
            if not message.reply_to_message:
                await message.reply("Balas pesan user yang ingin ditambahkan whitelist dengan perintah ini.")
                return
            add_whitelist(message.reply_to_message.from_user.id)
            await message.reply(f"User {message.reply_to_message.from_user.mention} ditambahkan ke whitelist.")

        elif cmd == "unwl":
            if not message.reply_to_message:
                await message.reply("Balas pesan user yang ingin dihapus whitelist dengan perintah ini.")
                return
            remove_whitelist(message.reply_to_message.from_user.id)
            await message.reply(f"User {message.reply_to_message.from_user.mention} dihapus dari whitelist.")

        elif cmd == "listwl":
            users = list_whitelist()
            if not users:
                await message.reply("Whitelist kosong.")
            else:
                await message.reply("Whitelist user IDs:\n" + "\n".join(str(u) for u in users))

        elif cmd == "dor":
            if not message.reply_to_message:
                await message.reply("Balas pesan user yang ingin ditambahkan blacklist pesan dengan perintah ini.")
                return
            add_blacklist_user(message.reply_to_message.from_user.id)
            await message.reply(f"User {message.reply_to_message.from_user.mention} ditambahkan ke blacklist pesan.")

        elif cmd == "undor":
            if not message.reply_to_message:
                await message.reply("Balas pesan user yang ingin dihapus blacklist pesan dengan perintah ini.")
                return
            remove_blacklist_user(message.reply_to_message.from_user.id)
            await message.reply(f"User {message.reply_to_message.from_user.mention} dihapus dari blacklist pesan.")

        elif cmd == "listdor":
            users = list_blacklist_user()
            if not users:
                await message.reply("Blacklist pesan kosong.")
            else:
                await message.reply("Blacklist pesan user IDs:\n" + "\n".join(str(u) for u in users))
