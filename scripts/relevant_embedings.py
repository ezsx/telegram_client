import os
import numpy as np
import psycopg2
from pgvector.psycopg2 import register_vector
from datetime import datetime, timedelta, timezone
import torch
import torch.nn.functional as F
from scripts.vectorize import vectorize_text


# Подключение к базе данных и настройка pgvector
conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)
register_vector(conn)
cursor = conn.cursor()

def get_recent_relevant_embeddings(user_query):
    # Вычисляем эмбеддинг запроса пользователя и преобразуем его в тензор
    query_embedding = vectorize_text(user_query)

    # Получаем текущее время и время 24 часа назад
    now = datetime.now(timezone.utc)
    yesterday = now - timedelta(days=1)

    # Извлекаем эмбеддинги новостей за последние 24 часа
    cursor.execute(
        """
        SELECT text, embedding FROM news
        WHERE published_at >= %s
        """, 
        (yesterday,)
    )
    rows = cursor.fetchall()

    relevant_embeddings = []
    
    # Проходим по каждой записи и рассчитываем косинусное расстояние
    for row in rows:
        news_text = row[0]
        news_embedding = torch.tensor(row[1], dtype=torch.float32)  # Преобразование в тензор
        similarity = F.cosine_similarity(query_embedding, news_embedding.unsqueeze(0)).item()
        relevant_embeddings.append((news_text, similarity))

    # Сортируем по релевантности (по убыванию схожести)
    relevant_embeddings.sort(key=lambda x: x[1], reverse=True)

    top_10_relevant_embedings = relevant_embeddings[:10]
    
    return top_10_relevant_embedings

