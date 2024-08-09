import os
from telethon import TelegramClient
import asyncio
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# Список каналов для скрейпинга (замените на ваши каналы)
channels = ['@rian_ru', '@tass_agency', '@rbc_news', '@kommersant']


async def fetch_messages(client, channel):
    channel_messages = []
    async for message in client.iter_messages(channel, limit=100):
        # Получаем информацию о канале
        channel_info = await client.get_entity(channel)
        channel_messages.append((channel_info.title, message))
    return channel_messages


async def main():
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start()

    all_messages = []
    for channel in channels:
        print(f"Fetching messages from {channel}...")
        messages = await fetch_messages(client, channel)
        all_messages.extend(messages)

    # Сортировка всех сообщений по дате отправки
    all_messages.sort(key=lambda x: x[1].date)

    # Вывод всех сообщений в порядке времени их появления
    for channel_name, message in all_messages:
        print(f"[{message.date}] {channel_name}: {message.text}")

    await client.disconnect()
    print("Client disconnected")


asyncio.run(main())
print("done")
