from utils.youtube_loader import YouTubeLoader

loader = YouTubeLoader()

url = input("Enter YouTube URL : ")

file = loader.save_transcript(url)

print("\nSaved Successfully")

print(file)