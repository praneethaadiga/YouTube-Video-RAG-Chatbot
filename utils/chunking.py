import json


class TranscriptChunker:

    def __init__(self, chunk_size=500):
        self.chunk_size = chunk_size

    def create_chunks(self, transcript_path, video_id):

        # Read transcript JSON
        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript = json.load(f)

        chunks = []

        current_text = ""
        current_start = None
        current_end = None
        chunk_id = 0

        for entry in transcript:

            text = entry["text"].strip()

            if not text:
                continue

            # Start timestamp of the chunk
            if current_start is None:
                current_start = entry["start"]

            # Add text
            if current_text:
                current_text += " "

            current_text += text

            # Latest timestamp
            current_end = entry["end"]

            # If chunk is large enough, save it
            if len(current_text) >= self.chunk_size:

                chunks.append(
                    {
                        "chunk_id": chunk_id,
                        "video_id": video_id,
                        "start_time": current_start,
                        "end_time": current_end,
                        "text": current_text
                    }
                )

                chunk_id += 1

                current_text = ""
                current_start = None
                current_end = None

        # Save remaining text
        if current_text:

            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "video_id": video_id,
                    "start_time": current_start,
                    "end_time": current_end,
                    "text": current_text
                }
            )

        return chunks