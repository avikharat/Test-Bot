import os
import json
from youtube_uploader import upload_video

def upload_all_shorts(base_dir=".", folder_prefix="short_"):
    for folder in sorted(os.listdir(base_dir)):
        if folder.startswith(folder_prefix):
            folder_path = os.path.join(base_dir, folder)
            video_path = os.path.join(folder_path, "output_captioned.mp4")  # updated name
            script_path = os.path.join(folder_path, "script.json")

            if not os.path.exists(video_path) or not os.path.exists(script_path):
                print(f"❌ Skipping {folder}: Missing video or script.json.")
                continue

            try:
                with open(script_path, "r", encoding="utf-8") as f:
                    script_data = json.load(f)

                title = script_data.get("title", "Untitled Shorts")
                description = script_data.get("story", "")
                tags = script_data.get("tags", [])

                # Final output before upload
                print(f"📤 Uploading: {video_path}")
                print(f"🔤 Title: {title}")
                print(f"📝 Description (preview): {description[:60]}...")
                #print(f🏷️ Tags: {tags}")

                # Upload
                upload_video(
                    file_path=video_path,
                    title=title,
                    description=description,
                    tags=tags,
                    privacy="public"
                )

                print(f"✅ Uploaded: {title}")

            except Exception as e:
                print(f"❌ Upload failed for {folder}: {e}")

if __name__ == "__main__":
    upload_all_shorts()
