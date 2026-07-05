import re


def extract_video_id(url):
    """
    Extracts the YouTube video ID from a standard or short URL.
    """
    pattern = (
        r"(?:https?://)?(?:www\.)?"
        r"(?:youtube\.com/watch\?v=|youtu\.be/)"
        r"([a-zA-Z0-9_-]{11})"
    )

    match = re.search(pattern, url)

    if match:
        return match.group(1)

    return None