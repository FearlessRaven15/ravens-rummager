

import os
import discord
from playwright.async_api import async_playwright

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])

URL = "https://palia.th.gl/rummage-pile?map=bahari-bay"

intents = discord.Intents.none()
client = discord.Client(intents=intents)


async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        page = await browser.new_page()

        print("🐦 Raven's Rummager")
        print("🌐 Loading THGL...")

        async def response_handler(response):
            url = response.url

            if "palia.th.gl" not in url:
                return

            if response.request.resource_type not in ["fetch", "xhr"]:
                return

            print()
            print("=" * 70)
            print("🌐 FETCH/XHR")
            print("=" * 70)
            print(url)
            print("STATUS:", response.status)

            try:
                text = await response.text()

                print("LENGTH:", len(text))

                # Zoek naar mogelijke data-objecten
                interesting = [
                    "rummage",
                    "chapaa",
                    "pile",
                    "marker",
                    "markers",
                    "locations",
                    "locations",
                    "filters",
                    "mapId",
                    "map_id",
                    "coordinates",
                ]

                lower = text.lower()

                found = [
                    word for word in interesting
                    if word.lower() in lower
                ]

                if found:
                    print("⭐ KEYWORDS:", ", ".join(found))
                    print()
                    print(text[:15000])

            except Exception as e:
                print("READ ERROR:", e)

        page.on("response", response_handler)

        await page.goto(
            URL,
            wait_until="networkidle",
            timeout=120000
        )

        await page.wait_for_timeout(20000)

        print()
        print("=" * 70)
        print("🐦 DONE")
        print("=" * 70)

        await browser.close()


async def main():
    await inspect()


@client.event
async def on_ready():
    try:
        await main()
    finally:
        await client.close()


client.run(DISCORD_TOKEN)
