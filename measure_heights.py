import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        await page.goto("http://localhost:4173")

        sections = await page.locator('.section').all()
        for i, section in enumerate(sections):
            id = await section.evaluate("el => el.id")
            box = await section.bounding_box()
            height = box['height'] if box else 0
            print(f"#{id} ({i}): {height}px")

        await browser.close()

asyncio.run(main())
