import os
import json
import openai
import random
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("Please set your OPENAI_API_KEY in a .env file or GitHub Secret")

client_openai = openai.OpenAI(api_key=OPENAI_API_KEY)

# Load topics
TOPICS_FILE = "topics.json"
if not os.path.exists(TOPICS_FILE):
    raise FileNotFoundError("Missing topics.json")

with open(TOPICS_FILE, "r") as f:
    TOPICS = json.load(f).get("topics", [])

if not TOPICS:
    raise ValueError("No topics found in topics.json")

# Used topics tracker
USED_TOPICS_FILE = "used_topics.json"
used_topics = set()
if os.path.exists(USED_TOPICS_FILE):
    with open(USED_TOPICS_FILE, "r") as f:
        try:
            used_topics = set(json.load(f))
        except:
            used_topics = set()

def get_unused_topic():
    unused = [t for t in TOPICS if t not in used_topics]
    if not unused:
        raise ValueError("🎉 All topics used!")
    return random.choice(unused)

def get_script_json(topic: str) -> dict:
    prompt = f"""
Use the topic: "{topic}"

Write a story of 140–160 words for a YouTube Shorts script of around 50 seconds. It must contain 100% true and fascinating 'Did You Know?' style facts. You can include multiple related facts in a single story to keep it engaging. The tone should be fun, casual, and natural — like something you'd hear in a TikTok or Reels narration. Avoid fluff, keep it punchy.

Return ONLY a valid JSON object in the following format:

{{
  "title": "Catchy title in ALL CAPS (under 8 words)",
  "story": "50-second narration in a natural TikTok-style tone, fun and engaging",
  "tags": ["relevant", "lowercase", "descriptive", "seo", "tags"]
}}
"""

    response = client_openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=500
    )

    content = response.choices[0].message.content.strip()

    if content.startswith("```"):
        content = content.strip("`").strip()
        if content.startswith("json"):
            content = content[4:].strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("❌ JSON decode failed. Content:\n", content)
        raise

def generate_scripts_json():
    global used_topics

    num_scripts = 5
    for i in range(1, num_scripts + 1):
        topic = get_unused_topic()
        print(f"🔍 Using topic: {topic}")

        folder = f"short_{i}"
        os.makedirs(folder, exist_ok=True)

        data = get_script_json(topic)

        file_path = os.path.join(folder, "script.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print(f"[✅] Saved: {file_path} — {data['title']}")
        used_topics.add(topic)

    with open(USED_TOPICS_FILE, "w") as f:
        json.dump(list(used_topics), f, indent=2)

if __name__ == "__main__":
    generate_scripts_json()
