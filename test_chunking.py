from utils.chunking import TranscriptChunker

VIDEO_ID = "aircAruvnKk"

TRANSCRIPT = "data/transcripts/aircAruvnKk.json"

chunker = TranscriptChunker(chunk_size=500)

chunks = chunker.create_chunks(
    TRANSCRIPT,
    VIDEO_ID
)

print("Total Chunks:", len(chunks))

print()

for chunk in chunks[:3]:

    print("=" * 60)

    print("Chunk ID:", chunk["chunk_id"])

    print("Start:", round(chunk["start_time"], 2))

    print("End:", round(chunk["end_time"], 2))

    print()

    print(chunk["text"])

    print()