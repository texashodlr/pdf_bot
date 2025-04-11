from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-MiniLM-L6-v2")

text = [doc["content"] for doc in docs]

embeddings = embedder.encode(texts, convert_to_numpy=True)