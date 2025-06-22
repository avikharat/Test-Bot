import json
import subprocess
import os

REELS_JSON = "reels_from_audio.json"
DOWNLOAD_DIR = "downloaded_reels"

def download_reel(url, output_path):
    try:
        cmd = [
            "yt-dlp",
            "--no-playlist",
            "-o", f"{output_path}/%(id)s.%(ext)s",
            url
        ]
        subprocess.run(cmd, check=True)
        print(f"✅ Downloaded: {url}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to download: {url}\n{e}")

def main():
    if not os.path.exists(REELS_JSON):
        print("❌ reels_from_audio.json not found.")
        return

    with open(REELS_JSON, "r") as f:
        urls = json.load(f)

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    for url in urls:
        download_reel(url, DOWNLOAD_DIR)

    print(f"\n📁 All done. Files saved to '{DOWNLOAD_DIR}'.")

if __name__ == "__main__":
    main()
