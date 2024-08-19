import asyncio
from scripts.fetch_messages import main as fetch_main
from scripts.db_operations import insert_messages_to_db


async def run_pipeline():
    messages = await fetch_main()  # Собираем новые сообщения после последней временной метки
    if messages:
        insert_messages_to_db(messages)  # Записываем только новые сообщения в базу данных
    else:
        print("No new messages to add.")


if __name__ == "__main__":
    asyncio.run(run_pipeline())
