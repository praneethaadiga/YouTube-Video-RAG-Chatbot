# from youtube_transcript_api import YouTubeTranscriptApi
# from utils.helper import extract_video_id
# import json
# import os


# class YouTubeLoader:

#     def __init__(self):

#         print("INSIDE INIT")

#         self.api = YouTubeTranscriptApi()

#         self.preferred_languages = [
#             "en",
#             "hi",
#             "kn",
#             "ta",
#             "te",
#             "ml",
#             "mr",
#             "bn",
#             "gu",
#             "pa"
#         ]

#         print(self.__dict__)

#     def get_transcript(self, youtube_url):

#         video_id = extract_video_id(youtube_url)

#         if video_id is None:
#             raise ValueError("Invalid YouTube URL")

#         try:

#             transcript_list = self.api.list(video_id)

#             print("\nAvailable transcripts:")

#             for t in transcript_list:
#                 print(
#                     t.language,
#                     t.language_code,
#                     t.is_generated
#                 )

#             transcript = None

#             # Try each preferred language individually
#             for lang in self.preferred_languages:

#                 try:

#                     transcript = transcript_list.find_generated_transcript([lang])

#                     print(f"Using generated transcript: {lang}")

#                     break

#                 except Exception:
#                     pass

#             # Try manually created transcripts
#             if transcript is None:

#                 for lang in self.preferred_languages:

#                     try:

#                         transcript = transcript_list.find_manually_created_transcript([lang])

#                         print(f"Using manual transcript: {lang}")

#                         break

#                     except Exception:
#                         pass

#             # Last fallback
#             if transcript is None:

#                 available = list(transcript_list)

#                 if not available:
#                     raise Exception("No transcript found.")

#                 transcript = available[0]

#                 print("Using first available transcript:",
#                     transcript.language)

#             fetched = transcript.fetch()

#             transcript_data = []

#             for entry in fetched:

#                 transcript_data.append(
#                     {
#                         "text": entry.text,
#                         "start": entry.start,
#                         "duration": entry.duration,
#                         "end": entry.start + entry.duration,
#                         "language": transcript.language,
#                         "language_code": transcript.language_code
#                     }
#                 )

#             return transcript_data

#         except Exception as e:

#             raise Exception(f"Transcript Error:\n{e}")

#     # def get_transcript(self, youtube_url):

#     #     print(">>> NEW MULTILINGUAL LOADER IS RUNNING <<<")
#     #     video_id = extract_video_id(youtube_url)

#     #     if video_id is None:
#     #         raise ValueError("Invalid YouTube URL")

#     #     try:

#     #         transcript_list = self.api.list(video_id)

#     #         transcript = None

#     #         # 1. Prefer generated transcripts
#     #         try:
#     #             transcript = transcript_list.find_generated_transcript(
#     #                 self.preferred_languages
#     #             )
#     #         except Exception:
#     #             pass

#     #         # 2. Then manually created transcripts
#     #         if transcript is None:
#     #             try:
#     #                 transcript = transcript_list.find_manually_created_transcript(
#     #                     self.preferred_languages
#     #                 )
#     #             except Exception:
#     #                 pass

#     #         # 3. Fallback to first available transcript
#     #         if transcript is None:

#     #             available = list(transcript_list)

#     #             if len(available) == 0:
#     #                 raise Exception("No transcript available.")

#     #             transcript = available[0]

#     #         fetched = transcript.fetch()

#     #         transcript_data = []

#     #         for entry in fetched:

#     #             transcript_data.append(
#     #                 {
#     #                     "text": entry.text,
#     #                     "start": entry.start,
#     #                     "duration": entry.duration,
#     #                     "end": entry.start + entry.duration,
#     #                     "language": transcript.language,
#     #                     "language_code": transcript.language_code
#     #                 }
#     #             )

#     #         return transcript_data

#     #     except Exception as e:
#     #         raise Exception(f"Transcript Error:\n{e}")

#     # def get_transcript(self, youtube_url):

#     #     print("=" * 60)
#     #     print("NEW get_transcript() is running")
#     #     print("=" * 60)

#     #     video_id = extract_video_id(youtube_url)

#     #     print("Video ID:", video_id)

#     #     transcript_list = self.api.list(video_id)

#     #     print("Available transcripts:")

#     #     for t in transcript_list:
#     #         print(
#     #             t.language,
#     #             t.language_code,
#     #             "Generated:", t.is_generated
#     #         )

#     def save_transcript(self, youtube_url):

#         video_id = extract_video_id(youtube_url)

#         transcript = self.get_transcript(youtube_url)

#         os.makedirs(
#             "data/transcripts",
#             exist_ok=True
#         )

#         filename = f"data/transcripts/{video_id}.json"

#         with open(
#             filename,
#             "w",
#             encoding="utf-8"
#         ) as f:

#             json.dump(
#                 transcript,
#                 f,
#                 indent=4,
#                 ensure_ascii=False
#             )

#         return filename






from youtube_transcript_api import YouTubeTranscriptApi
from utils.helper import extract_video_id
import json
import os


class YouTubeLoader:

    def __init__(self):

        print("=" * 60)
        print("YouTubeLoader initialized")
        print("=" * 60)

        self.api = YouTubeTranscriptApi()

        # Preferred transcript languages
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

            transcript_list = self.api.list(video_id)

            print("\nAvailable transcripts:")

            for t in transcript_list:
                print(
                    f"{t.language} ({t.language_code}) | Generated: {t.is_generated}"
                )

            transcript = None

            # ----------------------------
            # 1. Prefer generated transcript
            # ----------------------------
            for lang in self.preferred_languages:

                try:
                    transcript = transcript_list.find_generated_transcript([lang])
                    print(f"\nUsing generated transcript: {lang}")
                    break

                except Exception:
                    continue

            # ----------------------------
            # 2. Prefer manual transcript
            # ----------------------------
            if transcript is None:

                for lang in self.preferred_languages:

                    try:
                        transcript = transcript_list.find_manually_created_transcript([lang])
                        print(f"\nUsing manual transcript: {lang}")
                        break

                    except Exception:
                        continue

            # ----------------------------
            # 3. Fallback
            # ----------------------------
            if transcript is None:

                available = list(transcript_list)

                if len(available) == 0:
                    raise Exception("No transcript available.")

                transcript = available[0]

                print(
                    f"\nUsing first available transcript: {transcript.language}"
                )

            fetched = transcript.fetch()

            transcript_data = []

            for entry in fetched:

                transcript_data.append(
                    {
                        "text": entry.text,
                        "start": entry.start,
                        "duration": entry.duration,
                        "end": entry.start + entry.duration,
                        "language": transcript.language,
                        "language_code": transcript.language_code
                    }
                )

            print(f"\nTranscript lines: {len(transcript_data)}")

            return transcript_data

        except Exception as e:
            raise Exception(f"Transcript Error:\n{e}")

    def save_transcript(self, youtube_url):

        print("save_transcript() called")

        video_id = extract_video_id(youtube_url)

        transcript = self.get_transcript(youtube_url)

        os.makedirs("data/transcripts", exist_ok=True)

        filename = f"data/transcripts/{video_id}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                transcript,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(f"Transcript saved to {filename}")

        return filename