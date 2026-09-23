
import asyncio
import re

from playwright.async_api import async_playwright

THGL_URL = "https://palia.th.gl/rummage-pile?map=bahari-bay"


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("🐦‍⬛ Raven's Rummager")
        print("🔎 TH.GL JavaScript onderzoeken...")
        print()

        await page.goto(
            THGL_URL,
            wait_until="networkidle",
            timeout=120000
        )

        await page.wait_for_timeout(8000)

        scripts = await page.locator("script[src]").evaluate_all(
            """els => els.map(e => e.src).filter(Boolean)"""
        )

        scripts = list(dict.fromkeys(scripts))

        print(f"📦 JavaScript bestanden gevonden: {len(scripts)}")
        print()

        interesting = []

        keywords = [
            "/api/",
            "api.",
            "rummage",
            "pile",
            "location",
            "locations",
            "data-forge",
            "actors",
            "graphql",
            "fetch(",
            "axios",
        ]

        for i, script_url in enumerate(scripts, 1):
            print(f"[{i}/{len(scripts)}] {script_url}")

            try:
                response = await page.request.get(
                    script_url,
                    timeout=30000
                )

                if not response.ok:
                    print("   ❌ HTTP", response.status)
                    continue

                text = await response.text()

                found = []

                for keyword in keywords:
                    if keyword.lower() in text.lower():
                        found.append(keyword)

                if found:
                    print("   ⭐", ", ".join(found))
                    interesting.append((script_url, text))

            except Exception as e:
                print("   ⚠️", str(e))

        print()
        print("=" * 70)
        print("🔍 MOGELIJK INTERESSANTE API-ENDPOINTS")
        print("=" * 70)

        seen = set()

        url_pattern = re.compile(
            r'https?://[^"\'\\\s]+',
            re.IGNORECASE
        )

        api_pattern = re.compile(
            r'["\'`]([^"\'`]*?/api/[^"\'`]*)["\'`]',
            re.IGNORECASE
        )

        for script_url, text in interesting:

            matches = []

            matches.extend(url_pattern.findall(text))
            matches.extend(api_pattern.findall(text))

            for match in matches:
                clean = match.replace("\\/", "/")

                if (
                    "th.gl" in clean
                    or "/api/" in clean.lower()
                    or "actor" in clean.lower()
                    or "rummage" in clean.lower()
                    or "location" in clean.lower()
                    or "forge" in clean.lower()
                ):
                    if clean not in seen:
                        seen.add(clean)

                        print()
                        print("📌", clean[:1000])

        print()
        print("=" * 70)
        print(f"✅ Unieke interessante endpoints: {len(seen)}")
        print("=" * 70)

        await browser.close()


asyncio.run(main())
