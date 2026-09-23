
import os
import discord
from playwright.async_api import async_playwright

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])

THGL_URL = "https://palia.th.gl/rummage-pile"

intents = discord.Intents.none()
client = discord.Client(intents=intents)


async def inspect_thgl():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("🐦 Raven's Rummager starting...")
        print(f"🌐 Opening: {THGL_URL}")

        async def handle_response(response):
            url = response.url

            # Alleen de Rummage-pagina's bekijken
            if "/rummage-pile?map=" not in url:
                return

            print()
            print("=" * 60)
            print("🎯 RUMMAGE MAP RESPONSE FOUND!")
            print("=" * 60)
            print(f"URL: {url}")
            print(f"STATUS: {response.status}")

            try:
                body = await response.text()

                print(f"RESPONSE LENGTH: {len(body)}")

                lower_body = body.lower()

                keywords = [
                    "rummage",
                    "pile",
                    "location",
                    "latitude",
                    "longitude",
                    "coordinates",
                    "marker",
                    "position",
                    "x",
                    "y",
                    "z",
                ]

                for keyword in keywords:
                    print()
                    print("=" * 50)
                    print(f"🔎 SEARCH: {keyword.upper()}")
                    print("=" * 50)

                    start = 0
                    found = 0

                    while True:
                        position = lower_body.find(keyword, start)

                        if position == -1:
                            break

                        # Stukje vóór en na de gevonden tekst tonen
                        beginning = max(0, position - 500)
                        ending = min(len(body), position + 1500)

                        print(body[beginning:ending])
                        print("\n----------\n")

                        start = position + len(keyword)
                        found += 1

                        # Maximaal 10 resultaten per zoekwoord
                        if found >= 10:
                            break

                    if found == 0:
                        print("Geen resultaat gevonden.")

            except Exception as error:
                print(f"❌ Kon response niet lezen: {error}")

        page.on("response", handle_response)

        await page.goto(
            THGL_URL,
            wait_until="networkidle",
            timeout=120000
        )

        # Geef de dynamische kaart extra tijd om te laden
        await page.wait_for_timeout(15000)

        print()
        print("=" * 60)
        print("🐦 KLAAR MET THGL INSPECTIE")
        print("=" * 60)

        await browser.close()


async def main():
    await inspect_thgl()


@client.event
async def on_ready():
    try:
        await main()
    finally:
        await client.close()


client.run(DISCORD_TOKEN)
