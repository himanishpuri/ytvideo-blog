# yt_tool.py
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re

def extract_video_id(video_url: str) -> str:
    regex = r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})"
    match = re.search(regex, video_url)
    if not match:
        raise ValueError("Invalid YouTube URL.")
    return match.group(1)

def get_transcript(video_url: str, languages=['en']) -> str:
    video_id = extract_video_id(video_url)
    ytt_api = YouTubeTranscriptApi()
    try:
        fetched_transcript = ytt_api.fetch(video_id, languages=languages)
        
        formatter = TextFormatter()
        text = formatter.format_transcript(fetched_transcript)
        return text
    except Exception as e:
        raise RuntimeError(f"Transcript not available: {e}")
