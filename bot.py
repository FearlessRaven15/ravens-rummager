

import asyncio
import re

from playwright.async_api import async_playwright

THGL_URL = "https://palia.th.gl/rummage-pile?map=bahari-bay"


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        page = await browser.new_page()

        print("🐦‍⬛ Raven's Rummager")
        print("🔎 TH.GL Rummage-data zoeken...")
        print()

        await page.goto(
            THGL_URL,
            wait_until="networkidle",
            timeout=120000
        )

        await page.wait_for_timeout(8000)

        scripts = await page.locator(
            "script[src]"
        ).evaluate_all(
            """els => els.map(e => e.src).filter(Boolean)"""
        )

        scripts = list(dict.fromkeys(scripts))

        print(f"📦 Scripts gevonden: {len(scripts)}")
        print()

        found_any = False

        for i, script_url in enumerate(scripts, 1):

            try:
                response = await page.request.get(
                    script_url,
                    timeout=30000
                )

                if not response.ok:
                    continue

                text = await response.text()
                lower = text.lower()

                # Zoek alleen scripts die echt iets met Rummage/Pile te maken hebben
                important_words = [
                    "rummage",
                    "rummage-pile",
                    "rummagepile",
                    "pilelocation",
                    "pilelocations",
                    "pile-location",
                    "pile_location"
                ]

                matches = [
                    word for word in important_words
                    if word in lower
                ]

                if not matches:
                    continue

                found_any = True

                print()
                print("=" * 80)
                print("⭐ INTERESSANT SCRIPT")
                print("=" * 80)
                print(script_url)
                print()
                print("Gevonden woorden:", ", ".join(matches))
                print()

                # Toon stukjes code rond elk Rummage-resultaat
                shown = set()

                for word in matches:

                    start = 0

                    while True:

                        position = lower.find(word, start)

                        if position == -1:
                            break

                        snippet_start = max(0, position - 500)
                        snippet_end = min(
                            len(text),
                            position + 1000
                        )

                        snippet = text[
                            snippet_start:snippet_end
                        ]

                        # Geen identieke stukken dubbel tonen
                        clean_key = snippet[:300]

                        if clean_key not in shown:
                            shown.add(clean_key)

                            print("----- CODE RONDOM", word, "-----")
                            print(snippet)
                            print()
                            print("-" * 80)

                        start = position + len(word)

                        # Niet duizenden regels dumpen
                        if len(shown) >= 10:
                            break

                    if len(shown) >= 10:
                        break

        print()
        print("=" * 80)

        if found_any:
            print("🐦‍⬛ KLAAR — bovenstaande code is interessant!")
        else:
            print("❌ Geen Rummage-code gevonden.")

        print("=" * 80)

        await browser.close()


asyncio.run(main())
