# youtube_uploader.py

import os
from googleapiclient.http import MediaFileUpload
from youtube_service_auth import get_youtube_service_from_env

def upload_video(file_path, title, description, tags=None, privacy="public"):
    youtube = get_youtube_service_from_env()

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or ["AI Shorts", "Conspiracy", "Minecraft"],
            "categoryId": "24",  # Entertainment
        },
        "status": {
            "privacyStatus": privacy,
            "madeForKids": False,
        },
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype="video/*")

    print(f"📤 Uploading video: {title}")
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )
    response = request.execute()
    print(f"✅ Uploaded: https://youtube.com/watch?v={response['id']}")
