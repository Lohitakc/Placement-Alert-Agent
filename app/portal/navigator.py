from playwright.async_api import Page


class Navigator:

    def __init__(self, page: Page):
        self.page = page

    async def open_scheduled_companies(self):

        await self.page.get_by_role(
            "link",
            name="Scheduled Companies New"
        ).click()

        await self.page.wait_for_selector(
            "div.v-card.v-sheet.theme--light",
            timeout=10000
        )