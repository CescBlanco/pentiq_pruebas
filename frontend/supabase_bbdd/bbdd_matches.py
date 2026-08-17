from typing import Any
import re
from supabase_bbdd.database import supabase
import re
import os 
import time
import json
import asyncio

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
#----------------------------- FOTMOB---------------------------------------------------
COOKIES_FILE = "data/fotmob_cookies.json"
TABLE_NAME = "matches_raw_data"

def extract_match_id_fotmob(url: str) -> str:
    """
    Extract the FotMob match ID from a match URL.

    Args:
        url (str): FotMob match URL containing a match ID.

    Returns:
        str: Extracted match ID.

    Raises:
        TypeError: If url is not a string.
        ValueError: If a match ID cannot be extracted.
    """

    # 🔹 Validate input type
    if not isinstance(url, str):
        raise TypeError("url must be a string")

    match = re.search(r"#(\d+)", url)

    if not match:
        raise ValueError("Could not extract match ID from URL")

    return match.group(1)

async def fetch_match_json( url):
        from patchright.async_api import async_playwright
        """
        Fetch match details JSON data using Playwright.

        This function navigates to a match URL, listens for network responses
        containing match details data, and captures the corresponding JSON payload.
        It also manages cookies to maintain session persistence.

        Args:
            url (str): Match URL containing the match ID.

        Returns:
            dict: JSON data containing match details.

        Raises:
            TypeError: If url is not a string.
            ValueError: If match ID cannot be extracted from the URL.
            RuntimeError: If browser launch or navigation fails.
            Exception: If match data is not captured within the expected time.
        """

        # 🔹 Input validation
        if not isinstance(url, str):
            raise TypeError("url must be a string")
        

        match_id_match = re.search(r"#(\d+)", url).group(1)

        if not match_id_match:
            raise ValueError("Could not extract match ID from URL")
    
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch( headless=True)

            except Exception as e:
                raise RuntimeError(f"Failed to launch browser: {e}")
            
            context = await browser.new_context()

            # 🔹 Load cookies if available and valid
            if os.path.exists(COOKIES_FILE):

                mod_time = os.path.getmtime(COOKIES_FILE)

                if (time.time() - mod_time) / 3600 > 1:
                    os.remove(COOKIES_FILE)
                    print("🗑️ Cookies expired")

                else:
                    with open(COOKIES_FILE) as f:
                        cookies = json.load(f)
                    await context.add_cookies(cookies)
                    print("🍪 Cookies loaded")

            page = await context.new_page()

            # 🔹 Store captured responses
            captured = []

            async def handle_response(response):
                """
                Capture matchDetails responses from network traffic.
                """
                if "matchDetails" in response.url and f"matchId={match_id_match}" in response.url:
                    print(f"🔥 DETECTED: {response.url}")
                    try:
                        data = await response.json()
                        captured.append(data)
                    except Exception as e:
                        print(f"⚠️ Error reading JSON: {e}")

            page.on("response", handle_response)

            try:
                print("\n🌐 Surfing the internet...")
                 # 🔹 Navigate to match page
                await page.goto(url, wait_until="domcontentloaded")

                # 🔹 Wait up to 60 seconds for matchDetails response
                print("⏳ Waiting for matchDetails (resolves the Turnstile if it appears)...")
                for _ in range(600):  # 60 segundos
                    if captured:
                        break
                    await asyncio.sleep(0.1)

                if not captured:
                    raise Exception("Match data was not captured within 60 seconds")

                # 🔹 Save cookies
                cookies = await context.cookies()
                with open(COOKIES_FILE, "w") as f:
                    json.dump(cookies, f, indent=2)
                print("🍪 Save Cookies")

                print("✅ DATA READY")
                return captured[0]

            finally:
                # 🔹 Ensure browser is closed
                await browser.close()

#----------------------------WHOSCORED---------------------------------------------------

def extract_match_id(url):
    return re.search(r"/matches/(\d+)/", url).group(1)

def extract_match_dict_url(url):
    
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(15)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    
    element1 = soup.select_one('script:-soup-contains("formationIdNameMappings")')
    formation_mappings = json.loads(element1.text.split("formationIdNameMappings:")[1].split("}")[0] + "}")

    element2 = soup.select_one('script:-soup-contains("matchCentreEventTypeJson")')
    event_types_json  = json.loads(element2.text.split("matchCentreEventTypeJson: ")[1].split(",\n")[0])

    element = soup.select_one('script:-soup-contains("matchCentreData")')
    matchdict = json.loads(element.text.split("matchCentreData: ")[1].split(",\n")[0])

    players_dict = matchdict['playerIdNameDictionary']

    return formation_mappings, event_types_json, matchdict, players_dict

#----------------------------SUPABASE---------------------------------------------------
def save_match_cache(
    source: str,
    match_id: str,
    data: dict
) -> None:
    """
    Save or update raw match JSON in Supabase.

    Args:
        source: Data source ('fotmob' or 'whoscored').
        match_id: Match identifier from the source.
        data: Complete match JSON.

    Raises:
        TypeError: If arguments have invalid types.
        ValueError: If source or match_id is invalid.
        RuntimeError: If the data cannot be saved.
    """

    if not isinstance(source, str):
        raise TypeError("source must be a string")

    if not isinstance(match_id, str):
        raise TypeError("match_id must be a string")

    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary")

    source = source.strip().lower()
    match_id = match_id.strip()

    if source not in {"fotmob", "whoscored"}:
        raise ValueError(
            "source must be either 'fotmob' or 'whoscored'"
        )

    if not match_id:
        raise ValueError("match_id cannot be empty")

    try:
        response = (
            supabase
            .table(TABLE_NAME)
            .upsert(
                {
                    "source": source,
                    "match_id": match_id,
                    "data": data,
                },
                on_conflict="source,match_id",
            )
            .execute()
        )

    except Exception as e:
        raise RuntimeError(
            f"Failed to save {source} match cache: {e}"
        ) from e


def load_match_cache(source: str, match_id: str) -> dict | None:
    """
    Load raw match JSON from Supabase.
    Returns None if the match is not cached.
    """

    if not isinstance(source, str):
        raise TypeError("source must be a string")

    if not isinstance(match_id, str):
        raise TypeError("match_id must be a string")

    source = source.strip().lower()
    match_id = match_id.strip()

    if source not in {"fotmob", "whoscored"}:
        raise ValueError(
            "source must be either 'fotmob' or 'whoscored'"
        )

    if not match_id:
        raise ValueError("match_id cannot be empty")

    try:
        response = (
            supabase
            .table(TABLE_NAME)
            .select("data")
            .eq("source", source)
            .eq("match_id", match_id)
            .limit(1)
            .execute()
        )

        print("DEBUG response:", response)
        print("DEBUG response.data:", response.data)

    except Exception as e:
        raise RuntimeError(
            f"Failed to load {source} match cache: {e}"
        ) from e

    if not response.data:
        return None

    return response.data[0]["data"]