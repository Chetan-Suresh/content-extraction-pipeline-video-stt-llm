import os
from fastapi import APIRouter, BackgroundTasks
from app.services.audio_downloader import download_audio
from app.services.whisper_service import transcribe_audio
from app.services.parser import parse_recipe
from app.services.marketplace import generate_market_links

router = APIRouter()

def remove_file(path: str):
    """Helper to delete the temp audio file after the request is done."""
    try:
        if path and os.path.exists(path):
            os.remove(path)
            print(f"Deleted temp file: {path}")
    except Exception as e:
        print(f"Error deleting file: {e}")

@router.get("/api/extract")
def extract_recipe(video_url: str, background_tasks: BackgroundTasks):
    print(f"Processing URL: {video_url}")
    
    # 1. Download Audio
    audio_path = download_audio(video_url)

    if not audio_path:
        return {
            "status": "failed",
            "reason": "YouTube blocked audio extraction or FFMPEG is missing.",
            "recipe": None,
            "buy_links": []
        }

    try:
        # 2. Transcribe (Whisper)
        print("Transcribing...")
        transcript = transcribe_audio(audio_path)
        
        # 3. Parse (Groq AI)
        print("Analyzing with AI...")
        recipe = parse_recipe(transcript)
        
        # 4. Generate Links
        buy_links = generate_market_links(recipe)

        # Schedule cleanup
        background_tasks.add_task(remove_file, audio_path)

        return {
            "status": "success",
            "transcript_snippet": transcript[:200] + "...", # Preview only
            "recipe": recipe,
            "buy_links": buy_links
        }
        
    except Exception as e:
        # Ensure cleanup happens even if something fails
        background_tasks.add_task(remove_file, audio_path)
        return {"status": "error", "message": str(e)}
