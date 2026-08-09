import os

from dotenv import load_dotenv
from telethon import TelegramClient, events

from app.database.repository import TelegramRepository


load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")

GROUP_ID = 5237651230

MONITORED_NAMES = [
    "lohita chaudhari",
    "lohita",
    "lohi",
]

SHORTLIST_KEYWORDS = [
    "shortlist",
    "shortlisted",
    "selected candidates",
    "selection list",
    "shortlisted students",
]


class TelegramMonitor:

    def __init__(self):

        self.client = TelegramClient(
            "placement_agent",
            API_ID,
            API_HASH
        )

        self.repository = TelegramRepository()

    async def start(self):

        await self.client.start()

        print("Telegram connected successfully.")

        @self.client.on(events.NewMessage(chats=GROUP_ID))
        async def new_message_handler(event):

            message = event.message

            print("\n===== MESSAGE RECEIVED =====")
            print(f"Message ID: {message.id}")
            print(f"Text: {message.text}")

            if not message.text:
                print("Ignored: no text")
                return

            text = message.text
            text_lower = text.lower()

            name_matches = [
                name
                for name in MONITORED_NAMES
                if name in text_lower
            ]

            shortlist_matches = [
                keyword
                for keyword in SHORTLIST_KEYWORDS
                if keyword in text_lower
            ]

            print(f"Name matches: {name_matches}")
            print(f"Shortlist matches: {shortlist_matches}")

            # Ignore irrelevant messages
            if not name_matches and not shortlist_matches:
                return

            # Check duplicate
            if self.repository.message_exists(
                GROUP_ID,
                message.id
            ):
                print("Message already exists in database.")
                return

            telegram_message = {
                "telegram_message_id": message.id,
                "chat_id": GROUP_ID,
                "message_text": message.text,
                "message_date": message.date,
                "company_detected": 0,
                "name_mentioned": 1 if name_matches else 0,
                "shortlist_detected": 1 if shortlist_matches else 0,
            }

            self.repository.insert_message(telegram_message)

            print("✅ Message saved to database.")

            print("============================\n")

    async def stop(self):

        await self.client.disconnect()