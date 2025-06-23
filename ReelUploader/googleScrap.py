import random
import json
from googlesearch import search

KEYWORD_FILE = "keywords.json"
OUTPUT_FILE = "reelsLink.json"

def load_keywords(filepath):
    try:
        with open(filepath, "r") as f:
            keywords = json.load(f)
            if not isinstance(keywords, list):
                raise ValueError("Keywords file must contain a list")
            return keywords
    except Exception as e:
        print(f"❌ Failed to load keywords from {filepath}: {e}")
        return []

def collect_reel_links(keywords, target_count=20):
    reel_links = set()
    tried_keywords = set()

    while len(reel_links) < target_count and len(tried_keywords) < len(keywords):
        keyword = random.choice(keywords)
        if keyword in tried_keywords:
            continue
        tried_keywords.add(keyword)

        print(f"🔍 Searching: {keyword}")
        try:
            results = list(search(keyword, num_results=10))
            for url in results:
                if "/reel/" in url and "instagram.com" in url:
                    reel_links.add(url)
                    if len(reel_links) >= target_count:
                        break
        except Exception as e:
            print(f"⚠️ Search failed: {e}")

    return list(reel_links)

if __name__ == "__main__":
    search_keywords = load_keywords(KEYWORD_FILE)

    if not search_keywords:
        print("🚫 No keywords found. Exiting.")
    else:
        reels = collect_reel_links(search_keywords, target_count=10)

        with open(OUTPUT_FILE, "w") as f:
            json.dump(reels, f, indent=2)

        print(f"\n✅ Done. Found {len(reels)} reels.")
        print(f"📁 Saved to {OUTPUT_FILE}")
