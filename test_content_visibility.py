import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("http://localhost:4173")

        # We need to verify if the CSS is applied to .section
        # Not yet applied, so we will do this after modifying styles.css
        await browser.close()

asyncio.run(main())
