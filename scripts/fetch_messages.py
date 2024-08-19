import os
from telethon import TelegramClient
from dotenv import load_dotenv
from datetime import datetime
from sentence_transformers import SentenceTransformer
import psycopg2
from datetime import timedelta, timezone, tzinfo
from zoneinfo import ZoneInfo

# Загрузка переменных окружения
load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# Инициализация модели SBERT
model = SentenceTransformer('distiluse-base-multilingual-cased-v2')

# Список каналов для скрейпинга
channels = ['@rian_ru', '@tass_agency', '@rbc_news', '@kommersant']


def re_check():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    cursor = conn.cursor()

    cursor.execute("""SELECT table_schema, table_name
    FROM information_schema.tables
    WHERE table_name = 'news';""")
    print(cursor.fetchall())
    cursor.execute("SHOW search_path;")
    print(cursor.fetchall())

    # cursor.execute("SELECT MAX(published_at) FROM news")


def get_last_message_timestamp():
    """Функция для получения временной метки последнего сообщения в базе данных"""
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(published_at)::timestamptz FROM news")
    last_timestamp = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    return last_timestamp or datetime(2024,8,19,20,12,12,0, tzinfo=timezone.utc)  # Если нет данных, вернем минимальную дату

# Пример приведения since к offset-aware
async def fetch_messages(client, channel, since):
    """Функция для сбора сообщений из указанного канала после заданного времени"""
    since = get_last_message_timestamp()

    channel_messages = []
    async for message in client.iter_messages(channel):
        print(message.date)
        print(since)
        if message.date <= since:
            break
        channel_info = await client.get_entity(channel)
        embedding = model.encode(message.text, convert_to_tensor=True).tolist()
        channel_messages.append((channel_info.title, message.date, message.text, embedding))
    return channel_messages



async def main():
    """Основная функция для запуска процесса сбора сообщений"""
    # re_check()
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start()

    last_timestamp = get_last_message_timestamp()
    all_messages = []

    for channel in channels:
        print(f"Fetching messages from {channel}...")
        messages = await fetch_messages(client, channel, last_timestamp)
        all_messages.extend(messages)

    await client.disconnect()
    print("Client disconnected")

    return all_messages
