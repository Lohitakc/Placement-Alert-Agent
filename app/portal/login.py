from app.shared.config import PORTAL_PASSWORD, PORTAL_USERNAME


class LoginManager:

    async def login(self, page):

        await page.fill(
            "input[type='text']",
            PORTAL_USERNAME
        )

        await page.fill(
            "input[type='password']",
            PORTAL_PASSWORD
        )

        await page.click("button:has-text('LOGIN')")