from youtube_transcript_api import YouTubeTranscriptApi

video_id = "c35fpGWqXnk"

api = YouTubeTranscriptApi()

transcript_list = api.list(video_id)

print("Available transcripts:")

for t in transcript_list:
    print("---------------------")
    print("Language:", t.language)
    print("Code:", t.language_code)
    print("Generated:", t.is_generated)

print("\nTrying generated transcript...")

transcript = transcript_list.find_generated_transcript(["hi"])

data = transcript.fetch()

print("Success!")
print("Language:", transcript.language)
print("First line:")
print(data[0].text)