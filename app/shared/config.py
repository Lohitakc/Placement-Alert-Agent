from dotenv import load_dotenv
import os

load_dotenv()

PORTAL_USERNAME = os.getenv("PORTAL_USERNAME")
PORTAL_PASSWORD = os.getenv("PORTAL_PASSWORD")

LOGIN_URL = os.getenv("LOGIN_URL")

HEADLESS = os.getenv("HEADLESS", "False").lower() == "true"

SESSION_FILE = os.getenv(
    "SESSION_FILE",
    "data/sessions/portal_session.json"
)