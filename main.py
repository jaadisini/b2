import asyncio
from bot_manager import bot_utama, start_all_bots

async def main():
    await start_all_bots()
    await bot_utama.start()
    print("Bot utama dan semua bot berjalan...")
    await bot_utama.idle()

if __name__ == "__main__":
    asyncio.run(main())
