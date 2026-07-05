from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        print("Embedding model loaded successfully!")

    def embed_chunks(self, chunks):

        texts = []

        for chunk in chunks:
            texts.append(chunk["text"])

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True
        )

        return embeddings

    def embed_query(self, query):

        embedding = self.model.encode(
            query,
            convert_to_numpy=True
        )

        return embedding