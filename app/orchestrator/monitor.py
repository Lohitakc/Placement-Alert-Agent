import asyncio


class Monitor:

    def __init__(self, interval_minutes: int = 60):

        self.interval = interval_minutes * 60

    async def sleep(self):

        print(f"\nNext check in {self.interval // 60} minutes...\n")

        await asyncio.sleep(self.interval)