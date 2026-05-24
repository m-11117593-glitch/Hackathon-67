import asyncio
from collections import defaultdict
from urllib.parse import urlparse
import random


class WorkerPool:
    def __init__(self, max_global=10, max_per_domain=2):
        self.global_sem = asyncio.Semaphore(max_global)
        self.domain_sems = defaultdict(lambda: asyncio.Semaphore(max_per_domain))

    def get_domain(self, url: str):
        return urlparse(url).netloc

    async def run(self, url: str, func):
        domain = self.get_domain(url)

        async with self.global_sem:
            async with self.domain_sems[domain]:
                # jitter per domain (anti-bot)
                await asyncio.sleep(random.uniform(0.5, 1.5))
                return await func()