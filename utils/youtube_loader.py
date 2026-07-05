from youtube_transcript_api import YouTubeTranscriptApi
from utils.helper import extract_video_id
import json
import os


class YouTubeLoader:

    def __init__(self):

        self.api = YouTubeTranscriptApi()

        self.preferred_languages = [
            "en",
            "hi",
            "kn",
            "ta",
            "te",
            "ml",
            "mr",
            "bn",
            "gu",
            "pa"
        ]

    def get_transcript(self, youtube_url):

        video_id = extract_video_id(youtube_url)

        if video_id is None:
            raise ValueError("Invalid YouTube URL")

        try:

            # Try preferred languages first
            try:

                transcript = self.api.fetch(
                    video_id,
                    languages=self.preferred_languages
                )

            except Exception:

                # Fallback to ANY available transcript
                transcript = self.api.fetch(video_id)

            transcript_data = []

            language = getattr(transcript, "language", "Unknown")
            language_code = getattr(transcript, "language_code", "unknown")

            for entry in transcript:

                transcript_data.append(
                    {
                        "text": entry.text,
                        "start": entry.start,
                        "duration": entry.duration,
                        "end": entry.start + entry.duration,
                        "language": language,
                        "language_code": language_code
                    }
                )

            return transcript_data

        except Exception as e:

            raise Exception(f"Transcript Error:\n{e}")

    def save_transcript(self, youtube_url):

        video_id = extract_video_id(youtube_url)

        transcript = self.get_transcript(youtube_url)

        os.makedirs(
            "data/transcripts",
            exist_ok=True
        )

        filename = f"data/transcripts/{video_id}.json"

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                transcript,
                f,
                indent=4,
                ensure_ascii=False
            )

        return filename