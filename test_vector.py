from utils.chunking import TranscriptChunker
from utils.embeddings import EmbeddingGenerator
from utils.vector_db import VectorDatabase

VIDEO_ID = "aircAruvnKk"

TRANSCRIPT = "data/transcripts/aircAruvnKk.json"

print("Loading transcript...")

chunker = TranscriptChunker()

chunks = chunker.create_chunks(
    TRANSCRIPT,
    VIDEO_ID
)

print(f"Chunks : {len(chunks)}")

print()

embedder = EmbeddingGenerator()

embeddings = embedder.embed_chunks(chunks)

print()

db = VectorDatabase()

db.build_index(
    embeddings,
    chunks
)

db.save()

print()

db.load()

print()

while True:

    question = input("\nAsk Question (type exit to quit): ")

    if question.lower() == "exit":
        break

    query_vector = embedder.embed_query(
        question
    )

    results = db.search(
        query_vector,
        top_k=4
    )

    print()

    print("=" * 70)

    print("Retrieved Chunks")

    print("=" * 70)

    for result in results:

        minutes = int(result["start_time"] // 60)

        seconds = int(result["start_time"] % 60)

        print()

        print(f"Chunk ID : {result['chunk_id']}")

        print(
            f"Timestamp : {minutes}:{seconds:02d}"
        )

        print()

        print(result["text"])

        print()

        print("-" * 70)