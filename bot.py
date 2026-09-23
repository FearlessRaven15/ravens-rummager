import os
import asyncio
from datetime import datetime, timezone

import discord
from playwright.async_api import async_playwright

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])
THGL_URL = "https://palia.th.gl/rummage-pile"

intents = discord.Intents.none()
client = discord.Client(intents=intents)


async def fetch_rummage_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(THGL_URL, wait_until="networkidle", timeout=120000)
        await page.wait_for_timeout(5000)

        # Save visible text so we can inspect the page if THGL changes.
        text = await page.locator("body").inner_text()
        await browser.close()
        return text


def make_embed(page_text: str):
    # Initial version: send the captured THGL page text.
    # The exact location selectors/API can be refined once the live page
    # structure is confirmed in GitHub Actions.
    embed = discord.Embed(
        title="🐦‍⬛ Rummage Pile — Raven's Sanctuary",
        description=(
            "De Rummage Pile tracker is bijgewerkt.\n\n"
            "Bekijk de actuele locaties op THGL:\n"
            f"{THGL_URL}"
        ),
        url=THGL_URL,
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_footer(text="Raven's Rummager • THGL")
    return embed


async def main():
    page_text = await fetch_rummage_page()
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        channel = await client.fetch_channel(CHANNEL_ID)

    await channel.send(embed=make_embed(page_text))


@client.event
async def on_ready():
    try:
        await main()
    finally:
        await client.close()


client.run(DISCORD_TOKEN)
