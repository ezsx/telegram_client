import asyncio
from scripts.fetch_messages import main as fetch_main
from scripts.db_operations import insert_messages_to_db
from scripts.relevant_embedings import get_recent_relevant_embeddings

def print_results(relevant_embeddings):
    print("\nTop 10 Relevant News Articles:\n")
    final_sim=[]
    for i, (text, similarity) in enumerate(relevant_embeddings, 1):
        final_sim.append(float(similarity))
        print(f"{i}. Similarity: {similarity:.4f}")
        print(f"   Text: {text}\n")
        print("-" * 80)
    print(final_sim)

async def run_pipeline():
    messages = await fetch_main()  # Собираем новые сообщения после последней временной метки
    if messages:
        insert_messages_to_db(messages)  # Записываем только новые сообщения в базу данных
    else:
        print("No new messages to add.")

    # Поиск релевантных ембедингов
    user_query = "Что нового в экономике?"
    print("Запрос пользователя:" , user_query)
    relevant_embeddings = get_recent_relevant_embeddings(user_query)

    print_results(relevant_embeddings)


if __name__ == "__main__":
    asyncio.run(run_pipeline())
