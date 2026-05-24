import asyncio
import random
import logging
from playwright.async_api import async_playwright, Browser

from scraper.config import USER_AGENTS, MAX_CONCURRENCY

logger = logging.getLogger(__name__)


class PlaywrightClient:

    def __init__(self):
        self.semaphore = asyncio.Semaphore(MAX_CONCURRENCY)
        self.playwright = None
        self.browser: Browser = None
        self.context = None
        self.captured_urls = set()

    async def start(self):
        self.playwright = await async_playwright().start()

        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage"
            ]
        )

        self.context = await self.browser.new_context(
            user_agent=random.choice(USER_AGENTS),
            viewport={"width": 1366, "height": 768},
            java_script_enabled=True
        )

    async def attach_network_listener(self, page):

        async def handle_response(response):
            try:
                url = response.url

                if any(key in url.lower() for key in ["search", "listing", "property", "api"]):
                    text = await response.text()

                    if "mudah.my/property" in text:
                        import re
                        matches = re.findall(
                            r"https://www\.mudah\.my/property/[^\s\"']+",
                            text
                        )

                        for m in matches:
                            self.captured_urls.add(m.split("?")[0])

            except:
                pass

        page.on("response", lambda r: asyncio.create_task(handle_response(r)))

    async def auto_scroll(self, page):
        last_height = await page.evaluate("document.body.scrollHeight")

        for _ in range(4):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)

            new_height = await page.evaluate("document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height

    async def get_html(self, url: str) -> str:
        async with self.semaphore:

            await asyncio.sleep(random.uniform(1.2, 2.5))

            page = await self.context.new_page()

            try:
                await self.attach_network_listener(page)

                await page.goto(url, wait_until="domcontentloaded", timeout=60000)

                await page.wait_for_timeout(2500)

                await self.auto_scroll(page)
                await page.wait_for_timeout(1000)

                html = await page.content()

                if self.captured_urls:
                    extra_html = "".join(
                        f'<a href="{u}">{u}</a>' for u in self.captured_urls
                    )
                    html += extra_html
                    self.captured_urls.clear()

                return html

            except Exception as e:
                logger.warning(f"Fetch failed {url}: {e}")
                return ""

            finally:
                await page.close()

    async def stop(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()