from playwright.sync_api import sync_playwright
import time
import json
import os
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

USERNAME = os.getenv("INSTAGRAM_USERNAME")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

MAX_SCROLLS = 5
MAX_IDLE_SCROLLS = 2
SCROLL_PAUSE = 2

def login_to_instagram(page):
    print("🔐 Logging in to Instagram...")
    page.goto("https://www.instagram.com/accounts/login/", timeout=60000)
    page.wait_for_selector("input[name='username']", timeout=15000)
    page.fill("input[name='username']", USERNAME)
    page.fill("input[name='password']", PASSWORD)
    page.click("button[type='submit']")
    page.wait_for_selector("svg[aria-label='Home']", timeout=15000)
    print("✅ Login successful!")

def extract_reel_links(page, audio_page_url):
    print(f"🔗 Visiting: {audio_page_url}")
    page.goto(audio_page_url, timeout=60000)
    time.sleep(3)

    try:
        page.mouse.click(10, 10)  # Dismiss popups
        time.sleep(1)
    except Exception as e:
        print("⚠️ Failed to dismiss popup:", e)

    reel_links = set()
    idle_scrolls = 0

    for i in range(MAX_SCROLLS):
        new_links_found = 0
        anchors = page.query_selector_all("a._a6hd")

        for a in anchors:
            href = a.get_attribute("href")
            if href and "/reel/" in href:
                full_url = "https://www.instagram.com" + href
                if full_url not in reel_links:
                    reel_links.add(full_url)
                    new_links_found += 1

        print(f"🔁 Scroll {i+1}/{MAX_SCROLLS}: +{new_links_found} new, total = {len(reel_links)}")

        if new_links_found == 0:
            idle_scrolls += 1
        else:
            idle_scrolls = 0

        if idle_scrolls >= MAX_IDLE_SCROLLS:
            print("🚫 No new reels for a while — stopping early.")
            break

        page.mouse.wheel(0, 2500)
        time.sleep(SCROLL_PAUSE)

    return list(reel_links)

def main():
    parser = argparse.ArgumentParser(description="Scrape reels using Instagram Audio Page URL.")
    parser.add_argument(
        "--url", 
        required=False, 
        default="https://www.instagram.com/family.guy.reels/reels/",
        help="Instagram Audio Page URL to scrape reels from"
    )
    args = parser.parse_args()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login_to_instagram(page)
        reels = extract_reel_links(page, args.url)
        browser.close()

        with open("reels_from_audio.json", "w") as f:
            json.dump(reels, f, indent=2)

        print(f"\n✅ Done. Found {len(reels)} reels.")
        print("📁 Saved to reels_from_audio.json")

if __name__ == "__main__":
    main()
#py ReelURLFetcher.py --url "https://www.instagram.com/music/some.audio.page/reels/"