import subprocess
import uuid
import os
import sys

TEMP_DIR = "temp_audio"
os.makedirs(TEMP_DIR, exist_ok=True)

def download_audio(video_url: str) -> str | None:
    filename = f"{uuid.uuid4()}.m4a"
    output_path = os.path.join(TEMP_DIR, filename)

    # NOTE: We removed the hardcoded FFMPEG path. 
    # Make sure ffmpeg is installed and added to your System PATH variables.
    cmd = [
        sys.executable,
        "-m", "yt_dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "m4a",
        "-o", output_path,
        video_url
    ]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode != 0:
            print("yt-dlp error:", result.stderr)
            return None
            
        return output_path

    except FileNotFoundError:
        print("Error: yt-dlp or ffmpeg not found.")
        return None
