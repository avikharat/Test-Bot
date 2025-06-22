import os
import json
import random
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Load environment
load_dotenv()

# Load credentials
CLIENT_ID = os.getenv("YT_FG_CLIENT_ID")
CLIENT_SECRET = os.getenv("YT_FG_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("YT_FG_REFRESH_TOKEN")
VIDEO_DIR = "downloaded_reels"

# Title, description, tags pool
TITLES = [
    "Peter's Wildest Moments 😂",
    "Stewie Being a Savage Again 💀",
    "You Won’t Believe What Quagmire Did!",
    "Classic Cutaway Gag Compilation 😅",
    "Lois Snaps. Again. 😳",
    "Brian Has Had Enough 🐶",
    "Meg Gets Roasted... Again 💥",
    "Iconic Griffin Moments 🎬",
    "Best Family Guy Line Ever? 🤯",
    "Giggity Level 💯",
    "Peter Goes Full Psycho 😬",
    "Stewie’s Insult Game = Unmatched 🔥",
    "This Went Too Far 😂",
    "Only Family Guy Can Do This 💀",
    "Peter’s Brain Malfunctions Again 🤕",
    "Cutaway Gag of the Century 🧠",
    "Why Is Meg Always the Target? 😭",
    "Quagmire’s Most Awkward Moment Ever 🙈",
    "One Minute of Pure Griffin Chaos 🔥",
    "When Peter Thinks He’s Smart 😅"
]

DESCRIPTIONS = [
    "Another hilarious moment from Quahog. #FamilyGuy #Shorts",
    "Stewie might need therapy after this one 😂",
    "Peter Griffin at his finest. Don't miss it! #LOL",
    "Classic Family Guy cut that never gets old.",
    "Share if this made you laugh harder than you should have!",
    "Clip from one of the best Family Guy episodes ever. 🔥",
    "Giggity. Giggity. Watch till the end!",
    "The most random Family Guy scene you’ll ever see 🤣",
    "Comment your favorite moment! #PeterGriffin",
    "This is why we love Family Guy. Period."
]

TAGS_POOL = [
    ["family guy", "shorts", "funny", "peter griffin", "stewie"],
    ["quahog", "cutaway gag", "griffins", "comedy", "short"],
    ["lois", "meg", "brian", "quagmire", "lol"],
    ["animated comedy", "cartoon", "fox", "tv clip", "reels"],
    ["peter", "savage moments", "stewie griffin", "viral", "trending"]
]

def get_authenticated_service():
    creds = Credentials(
        None,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )
    creds.refresh(Request())
    return build("youtube", "v3", credentials=creds)

def get_random_metadata():
    title = random.choice(TITLES)
    description = random.choice(DESCRIPTIONS)
    tags = random.choice(TAGS_POOL)
    return title, description, tags

def upload_video(youtube, video_path):
    title, description, tags = get_random_metadata()

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "23"  # Comedy
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)

    try:
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
        response = request.execute()
        print(f"✅ Uploaded: {video_path} → https://youtube.com/watch?v={response['id']}")
        return True
    except Exception as e:
        print(f"❌ Upload failed for: {video_path}\n{e}")
        return False

def main():
    youtube = get_authenticated_service()

    video_files = [
        f for f in os.listdir(VIDEO_DIR)
        if f.lower().endswith((".mp4", ".mov"))
    ]

    for video_file in video_files:
        video_path = os.path.join(VIDEO_DIR, video_file)
        success = upload_video(youtube, video_path)

        if not success:
            print("🚫 Stopping further uploads due to failure.")
            break

if __name__ == "__main__":
    main()
