from utils.chunking import TranscriptChunker
from utils.embeddings import EmbeddingGenerator
from utils.vector_db import VectorDatabase
from utils.rag import RAG

VIDEO_ID = "aircAruvnKk"

TRANSCRIPT = "data/transcripts/aircAruvnKk.json"

print("Loading transcript...")

chunker = TranscriptChunker()

chunks = chunker.create_chunks(
    TRANSCRIPT,
    VIDEO_ID
)

print(f"Chunks Created : {len(chunks)}")

print()

embedder = EmbeddingGenerator()

embeddings = embedder.embed_chunks(chunks)

print()

db = VectorDatabase()

db.build_index(
    embeddings,
    chunks
)

print()

rag = RAG()

while True:

    question = input("\nAsk Question (type exit to quit): ")

    if question.lower() == "exit":
        break

    query_embedding = embedder.embed_query(question)

    retrieved_chunks = db.search(
        query_embedding,
        top_k=4
    )

    answer = rag.answer(
        retrieved_chunks,
        question
    )

    print()

    print("=" * 80)

    print("Answer")

    print("=" * 80)

    print()

    print(answer)

    print()

    print("=" * 80)

    print("Retrieved Sources")

    print("=" * 80)

    for chunk in retrieved_chunks:

        minutes = int(chunk["start_time"] // 60)

        seconds = int(chunk["start_time"] % 60)

        print(
            f"\nTimestamp : {minutes}:{seconds:02d}"
        )

        print(chunk["text"][:250])

        print("-" * 80)