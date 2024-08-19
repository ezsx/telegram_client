-- Создание расширения pgvector, если его еще нет
CREATE EXTENSION IF NOT EXISTS vector;

-- Создание таблицы news
CREATE TABLE IF NOT EXISTS news
(
    id           SERIAL PRIMARY KEY,
    published_at TIMESTAMP,
    text         TEXT,
    embedding    VECTOR(512) -- distiluse-base-multilingual-cased-v2 из библиотеки Sentence-Transformers.
    -- Размер эмбеддинга этой модели фиксирован и составляет 512.
);

SHOW search_path;
