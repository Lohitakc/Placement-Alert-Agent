from playwright.async_api import Page
from app.portal.company_parser import CompanyParser


class Extractor:

    def __init__(self, page: Page):
        self.page = page

    async def extract_companies(self):

        companies = []

        cards = self.page.locator("div.v-card.v-sheet.theme--light")

        count = await cards.count()

        for i in range(count):

            card = cards.nth(i)

            company_name = (
                await card.locator(".v-card__title").inner_text()
            ).strip()

            company_type = (
                await card.locator(".v-card__subtitle").inner_text()
            ).strip()

            details = await card.locator(".ma-1").all_inner_texts()

            more_button = card.get_by_role("button", name="More")

            async with self.page.expect_response(
                lambda r: "CompanyofferingInfo" in r.url and r.status == 200
            ) as info_resp, self.page.expect_response(
                lambda r: "getCompanyOfferingForFileAttachment" in r.url and r.status == 200
            ) as attach_resp:
                await more_button.click()

            await info_resp.value
            await attach_resp.value

            parser = CompanyParser(self.page)

            full_details = await parser.parse()

            await self.page.go_back()

            await self.page.wait_for_url("**/apply_company")

            await self.page.wait_for_selector("div.v-card.v-sheet.theme--light")

            companies.append(
                {
                    "company_name": company_name,
                    "company_type": company_type,
                    "details": details,
                    "full_details": full_details,
                }
            )

        return companies