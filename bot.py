
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
            request_type = response.request.resource_type

            if request_type not in {"xhr", "fetch"}:
                return

            print()
            print("🔎 NETWORK REQUEST")
            print(f"Status: {response.status}")
            print(f"Type:   {request_type}")
            print(f"URL:    {response.url}")

            content_type = response.headers.get("content-type", "")

            if "json" in content_type:
                try:
                    body = await response.text()

                    keywords = [
                        "rummage",
                        "pile",
                        "chapaa",
                        "kilima",
                        "bahari",
                        "elderwood",
                        "highlands",
                        "location",
                        "coordinate",
                    ]

                    lower_body = body.lower()

                    if any(keyword in lower_body for keyword in keywords):
                        print("⭐ POSSIBLE RUMMAGE DATA FOUND!")
                        print(body[:10000])

                except Exception as e:
                    print(f"Could not read response: {e}")

        page.on("response", handle_response)

        await page.goto(
            THGL_URL,
            wait_until="networkidle",
            timeout=120000
        )

        print("✅ Page loaded.")

        # Give the dynamic map/API time to load.
        await page.wait_for_timeout(10000)

        print()
        print("========== PAGE TEXT ==========")

        text = await page.locator("body").inner_text()
        print(text[:15000])

        print()
        print("========== END DEBUG ==========")

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
