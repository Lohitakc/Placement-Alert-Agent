from playwright.async_api import async_playwright
from app.portal.navigator import Navigator
from app.portal.extractor import Extractor
from app.portal.login import LoginManager
from app.portal.session import SessionManager
from app.shared.config import HEADLESS, LOGIN_URL


class Portal:

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

        self.session = SessionManager()
        self.login_manager = LoginManager()

    async def start(self):

        self.playwright = await async_playwright().start()

        self.browser = await self.playwright.chromium.launch(
            headless=HEADLESS
        )

        if self.session.session_exists():

            self.context = await self.browser.new_context(
                storage_state=str(self.session.session_path)
            )

        else:

            self.context = await self.browser.new_context()

        self.page = await self.context.new_page()
        self.navigator = Navigator(self.page)
        self.extractor = Extractor(self.page)
        await self.page.goto(LOGIN_URL)

        if await self.page.locator("button:has-text('LOGIN')").count() > 0:

            await self.login_manager.login(self.page)
            await self.session.save(self.context)

    async def stop(self):

        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()

    async def open_scheduled_companies(self):
        await self.navigator.open_scheduled_companies()

    async def get_companies(self):
        return await self.extractor.extract_companies()