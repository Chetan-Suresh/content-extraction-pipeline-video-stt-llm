from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    CouldNotRetrieveTranscript
)


def extract_video_id(url: str) -> str:
    # Standard YouTube watch
    if "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]

    # youtu.be short link
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]

    # Shorts
    if "youtube.com/shorts/" in url:
        return url.split("youtube.com/shorts/")[1].split("?")[0]

    raise Exception("Invalid YouTube URL format")


def fetch_transcript(url: str) -> str:
    video_id = extract_video_id(url)

    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([i["text"] for i in transcript_list])
        return full_text

    except (TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript):
        return ""  # Return empty transcript instead of crashing
