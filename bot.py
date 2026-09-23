


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

            if "/rummage-pile?map=" not in url:
                return

            print()
            print("========================================")
            print("🎯 RUMMAGE MAP RESPONSE FOUND!")
            print("========================================")
            print(f"URL: {url}")
            print(f"STATUS: {response.status}")

            try:
                body = await response.text()

                print()
                print("========== RESPONSE BODY ==========")
                print(body[:30000])
                print("========== END RESPONSE ==========")

            except Exception as e:
                print(f"❌ Could not read response: {e}")

        page.on("response", handle_response)

        await page.goto(
            THGL_URL,
            wait_until="networkidle",
            timeout=120000
        )

        await page.wait_for_timeout(10000)

        print()
        print("🐦 Finished inspecting Rummage data.")

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
