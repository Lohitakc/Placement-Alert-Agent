import os

from dotenv import load_dotenv
from telethon import TelegramClient, events
from app.notifications.notifier import Notifier
from app.database.database import get_connection
from app.database.repository import TelegramRepository


load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")

# Temporary test chat
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
        self.notifier = Notifier()

    async def start(self):

        await self.client.start()

        print("Telegram connected successfully.")

        @self.client.on(events.NewMessage(chats=GROUP_ID))
        async def new_message_handler(event):

            message = event.message

            if not message.text:
                return

            text = message.text
            text_lower = text.lower()

            # -----------------------------
            # Name detection
            # -----------------------------

            name_matches = [
                name
                for name in MONITORED_NAMES
                if name in text_lower
            ]

            # -----------------------------
            # Shortlist detection
            # -----------------------------

            shortlist_matches = [
                keyword
                for keyword in SHORTLIST_KEYWORDS
                if keyword in text_lower
            ]

            # -----------------------------
            # Company detection
            # -----------------------------

            company_matches = self.find_company_matches(text_lower)

            # -----------------------------
            # Ignore irrelevant messages
            # -----------------------------

            if (
                not name_matches
                and not shortlist_matches
                and not company_matches
            ):
                return

            # -----------------------------
            # Duplicate protection
            # -----------------------------

            if self.repository.message_exists(
                GROUP_ID,
                message.id
            ):
                print(
                    f"Message {message.id} "
                    "already exists in database."
                )
                return

            # -----------------------------
            # Save relevant message
            # -----------------------------

            telegram_message = {
                "telegram_message_id": message.id,
                "chat_id": GROUP_ID,
                "message_text": text,
                "message_date": message.date,
                "company_detected": 1 if company_matches else 0,
                "name_mentioned": 1 if name_matches else 0,
                "shortlist_detected": 1 if shortlist_matches else 0,
            }

            self.repository.insert_message(
                telegram_message
            )

            # -----------------------------
            # Debug output
            # -----------------------------

            print("\n===== RELEVANT TELEGRAM MESSAGE =====")

            print(f"Message ID: {message.id}")
            print(f"Date: {message.date}")
            print(f"Text: {text}")

            if company_matches:
                print("🏢 COMPANY DETECTED")
                print(
                    f"Matched: {', '.join(company_matches)}"
                )

            if name_matches:
                print("🔴 NAME MENTION DETECTED")
                print(
                    f"Matched: {', '.join(name_matches)}"
                )

            if shortlist_matches:
                print("🟡 SHORTLIST MESSAGE DETECTED")
                print(
                    f"Matched: {', '.join(shortlist_matches)}"
                )

            print("✅ Saved to database.")
            print("=====================================\n")

            if company_matches:

                self.notifier.send(
                    "🏢 Company Announcement",
                    f"{', '.join(company_matches)}\n\n{text}"
                )

            if name_matches:

                self.notifier.send(
                    "🔴 Your Name Mentioned",
                    text
                )

            if shortlist_matches:

                self.notifier.send(
                    "🟡 Shortlist Released",
                    text
                )

    def find_company_matches(self, text_lower):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT company_name
            FROM companies
            WHERE company_name IS NOT NULL
            AND company_name != ''
            """
        )

        companies = cursor.fetchall()

        connection.close()

        matches = []

        for company in companies:

            company_name = company["company_name"].strip()

            if not company_name:
                continue

            if company_name.lower() in text_lower:
                matches.append(company_name)

        return matches

    async def stop(self):

        await self.client.disconnect()