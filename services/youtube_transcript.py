from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from urllib.parse import urlparse, parse_qs


def extract_video_id(youtube_url):
    try:
        parsed_url = urlparse(youtube_url)
        if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
            return parse_qs(parsed_url.query).get("v", [None])[0]
        elif parsed_url.hostname == "youtu.be":
            return parsed_url.path.lstrip('/')
        else:
            return None
    except Exception:
        return None


def get_transcript_text(video_url, languages=['fr', 'en']):
    video_id = extract_video_id(video_url)
    if not video_id:
        raise ValueError("Lien YouTube invalide.")

    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
    return "\n".join([entry['text'] for entry in transcript])
