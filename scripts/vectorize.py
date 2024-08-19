from sentence_transformers import SentenceTransformer

model = SentenceTransformer('distiluse-base-multilingual-cased-v2')


def vectorize_text(text):
    return model.encode(text, convert_to_tensor=True).tolist()
