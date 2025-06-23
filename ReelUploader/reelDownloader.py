import json
import subprocess
import os

REELS_JSON = "reelsLink.json"
DOWNLOAD_DIR = "downloaded_reels"

def download_reel(url, output_path):
    try:
        cmd = [
            "yt-dlp",
            "--force-generic-extractor",
            "--no-playlist",
            "-o", f"{output_path}/%(id)s.%(ext)s",
            url
        ]
        subprocess.run(cmd, check=True)
        print(f"✅ Downloaded: {url}")
    except subprocess.CalledProcessError:
        print(f"❌ Skipped (not public or failed): {url}")

def main():
    if not os.path.exists(REELS_JSON):
        print(f"❌ {REELS_JSON} not found.")
        return

    with open(REELS_JSON, "r") as f:
        urls = json.load(f)

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    print(f"📥 Starting download of {len(urls)} reels...\n")

    for url in urls:
        download_reel(url, DOWNLOAD_DIR)

    print(f"\n✅ All done. Check '{DOWNLOAD_DIR}' for downloaded videos.")

if __name__ == "__main__":
    main()
