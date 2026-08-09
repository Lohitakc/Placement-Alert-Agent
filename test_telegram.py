import asyncio

from app.telegram.monitor import TelegramMonitor


async def main():

    monitor = TelegramMonitor()

    await monitor.start()

    print("Waiting for new Telegram messages...")

    await monitor.client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())