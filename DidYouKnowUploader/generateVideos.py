import os
import json
import random
import requests
import base64
import time
from dotenv import load_dotenv

load_dotenv()

DID_API_KEY = os.getenv("DID_API_KEY")
if not DID_API_KEY:
    raise EnvironmentError("Missing environment variable: DID_API_KEY")

def download_did_clip(clip_id: str, api_key: str, output_path: str):
    url = f"https://api.d-id.com/clips/{clip_id}"
    headers = {
        "accept": "application/json",
        "authorization": "Basic " + base64.b64encode(f"{api_key}:".encode()).decode()
    }

    print(f"[*] Waiting for clip '{clip_id}' to finish processing...")

    for attempt in range(30):
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "done":
            result_url = data.get("result_url")
            print(f"[+] Clip is ready! Downloading from: {result_url}")
            break
        else:
            print(f"    Attempt {attempt + 1}/30 — Status: {data.get('status')}")
            time.sleep(2)
    else:
        raise TimeoutError("[-] Clip did not finish processing in time.")

    video = requests.get(result_url)
    video.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(video.content)

    print(f"[+] Clip saved to: {output_path}")
    return output_path


def select_presenter_and_voice(presenters_file="presenters.json", voices_file="voices.json"):
    with open(presenters_file, "r") as f:
        presenters = json.load(f)["presenters"]

    with open(voices_file, "r") as f:
        voices = json.load(f)["voices"]

    presenter = random.choice(presenters)
    presenter_gender = presenter.get("gender", "").lower()

    matching_voices = [
        v for v in voices if v.get("labels", {}).get("gender", "").lower() == presenter_gender
    ]
    if not matching_voices:
        raise Exception(f"No matching voice found for gender: {presenter_gender}")

    voice = random.choice(matching_voices)

    return presenter, voice


def create_clip(script_text, output_path):
    presenter, voice = select_presenter_and_voice()
    presenter_id = presenter["presenter_id"]
    voice_id = voice["voice_id"]

    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{DID_API_KEY}:".encode()).decode(),
        "Content-Type": "application/json"
    }

    payload = {
        "script": {
            "type": "text",
            "input": script_text,
            "provider": {
                "type": "elevenlabs",
                "voice_id": voice_id
            }
        },
        "presenter_id": presenter_id,
        "config": {
            "fluent": True,
            "pad_audio": 0.2,
            "result_format": "webm"
        },
        "presenter_config": {
            "crop": {
                "type": "wide"
            }
        },
        "background": {
            "source_url": "https://res.cloudinary.com/dtfum7lfk/image/upload/v1750570765/pexels-atbo-66986-245240_rg7kgd.jpg"
        }
    }

    response = requests.post("https://api.d-id.com/clips", headers=headers, json=payload)

    if response.ok:
        data = response.json()
        clip_id = data.get("id")
        print("✅ Clip created!")
        return download_did_clip(clip_id, DID_API_KEY, output_path)
    else:
        print("❌ Failed to create clip:")
        print(response.status_code, response.text)
        return None


def generate_clips_from_scripts(base_dir="."):
    for folder in os.listdir(base_dir):
        if folder.startswith("short_") and os.path.isdir(folder):
            json_path = os.path.join(folder, "script.json")
            output_path = os.path.join(folder, f"{folder}.mp4")

            if not os.path.exists(json_path):
                print(f"⚠️ Skipping {folder} — script.json not found.")
                continue

            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            story = data.get("story", "").strip()
            if not story:
                print(f"⚠️ Skipping {folder} — 'story' is missing.")
                continue

            print(f"\n🎬 Generating video for {folder}...")
            create_clip(script_text=story, output_path=output_path)


if __name__ == "__main__":
    generate_clips_from_scripts()
