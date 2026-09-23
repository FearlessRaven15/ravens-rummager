

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

        requests = []

        async def handle_request(request):
            url = request.url

            if "palia.th.gl" in url:
                requests.append((request.resource_type, url))

        page.on("request", handle_request)

        await page.goto(
            THGL_URL,
            wait_until="networkidle",
            timeout=120000
        )

        await page.wait_for_timeout(10000)

        print()
        print("========== ALL THGL RESOURCES ==========")

        for resource_type, url in requests:
            print(f"[{resource_type}] {url}")

        print()
        print("========== PERFORMANCE RESOURCES ==========")

        resources = await page.evaluate("""
            () => performance.getEntriesByType('resource')
                .map(x => x.name)
                .filter(x => x.includes('palia.th.gl'))
        """)

        for url in resources:
            print(url)

        print()
        print("========== JAVASCRIPT FILES ==========")

        scripts = await page.locator("script[src]").evaluate_all(
            "(els) => els.map(e => e.src)"
        )

        for url in scripts:
            print(url)

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
