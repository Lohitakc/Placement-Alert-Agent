import asyncio

from rich import print

from app.telegram.monitor import TelegramMonitor


async def main():

    monitor = TelegramMonitor()

    try:

        await monitor.start()

        print("Waiting for new Telegram messages...")

        await monitor.client.run_until_disconnected()

    except (KeyboardInterrupt, asyncio.CancelledError):

        print("\nTelegram monitor stopped by user.")

    finally:

        await monitor.stop()


if __name__ == "__main__":

    try:
        asyncio.run(main())

    except KeyboardInterrupt:

        print("\nTelegram monitor stopped by user.")