from pathlib import Path

from playwright.async_api import Browser

from app.shared.config import SESSION_FILE


class SessionManager:

    def __init__(self):
        self.session_path = Path(SESSION_FILE)

    def session_exists(self) -> bool:
        return self.session_path.exists()

    async def save(self, browser_context):
        self.session_path.parent.mkdir(parents=True, exist_ok=True)

        await browser_context.storage_state(
            path=str(self.session_path)
        )