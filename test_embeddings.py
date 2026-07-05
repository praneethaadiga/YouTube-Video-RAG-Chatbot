from utils.chunking import TranscriptChunker
from utils.embeddings import EmbeddingGenerator

VIDEO_ID = "aircAruvnKk"

TRANSCRIPT = "data/transcripts/aircAruvnKk.json"

print("Creating chunks...")

chunker = TranscriptChunker()

chunks = chunker.create_chunks(
    TRANSCRIPT,
    VIDEO_ID
)

print(f"Chunks Created: {len(chunks)}")

print()

embedder = EmbeddingGenerator()

embeddings = embedder.embed_chunks(chunks)

print()

print("Embedding Shape:")

print(embeddings.shape)

print()

print("First Embedding:")

print(embeddings[0][:15])