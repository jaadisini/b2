from pyrogram import Client, filters
from pyrogram.types import Message
from db import (
    get_group_status, add_whitelist, remove_whitelist, list_whitelist,
    add_blacklist_user, remove_blacklist_user, list_blacklist_user,
    add_blacklist_trigger, remove_blacklist_trigger, list_blacklist_trigger,
    set_group_status
)

def is_gcast_message(text: str, triggers: list) -> bool:
    bl = "€¥£¢𝑎𝑏𝑐𝑑𝑒𝑓𝑔𝒉𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ×̰͓̰̈́̈́̈́̈́ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯 🇰 🇱 🇲 🇳 🇴 🇵 🇶 🇷 🇸 🇹 🇺 🇻 🇼 🇽 🇾 🇿 🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯 🇰 🇱 🇲 🇳 🇴 🇵 🇶 🇷 🇸 🇹 🇺 🇻 🇼 🇽 🇾 🇿 ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘϙʀᴛᴜᴠᴡʏᴢᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘϙʀᴛᴜᴠᴡʏᴢᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘϙʀᴛᴜᴠᴡʏᴢᗩᗷᑕᗞᗴᖴᏀᕼᏆᒍᏦしᗰᑎᝪᑭᑫᖇᔑᎢᑌᐯᗯ᙭ᎩᏃᗩᗷᑕᗞᗴᖴᏀᕼᏆᒍᏦしᗰᑎᝪᑭᑫᖇᔑᎢᑌᐯᗯ᙭ᎩᏃᎪᏴᏟᎠᎬҒᏀᎻᏆᎫᏦᏞᎷΝϴᏢϘᎡՏͲႮᏙᏔХᎽᏃᎪᏴᏟᎠᎬҒᏀᎻᏆᎫᏦᏞᎷΝϴᏢϘᎡՏͲႮᏙᏔХᎽᏃａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁"
    awoos = update.text
    x = awoos.lower()

        
    with open('bl.txt', 'r') as file:
        blc = [w.lower().strip() for w in file.readlines()]
        for chara in bl:
            blc.append(chara)

    for chara in blc:
        if chara in x:
            return True
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
