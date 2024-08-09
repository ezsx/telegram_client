import os
from telethon import TelegramClient
import asyncio
from dotenv import load_dotenv

# Вставьте ваши API_ID и API_HASH, полученные на my.telegram.org

load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# Список каналов для скрейпинга
channels2 = ['@rian_ru']
channels = ['@rian_ru', '@tass_agency', '@rbc_news', '@kommersant']


async def fetch_messages(client, channel):
    async for message in client.iter_messages(channel, limit=100):
        print(f"Channel: {channel}, Message: {message.text}")


async def main():
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start()

    tasks = [fetch_messages(client, channel) for channel in channels]
    await asyncio.gather(*tasks)

    await client.disconnect()


asyncio.run(main())
print("done")
