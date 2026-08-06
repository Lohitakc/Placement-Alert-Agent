from playwright.async_api import Page

class CompanyParser:

    def __init__(self, page: Page):
        self.page = page

    async def parse(self):

        await self.page.wait_for_url("**/company-info")

        company_information = await self.extract_company_information()

        return {
            "company_information": company_information
        }

    async def extract_company_information(self):

        info = {}

        card = self.page.locator(
            "div.v-card:has-text('Company Information And Criteria')"
        )

        rows = card.locator("div.row")

        row_count = await rows.count()

        for i in range(row_count):

            row = rows.nth(i)

            row_text = (await row.inner_text()).strip()

            # Stop before Eligible Branches
            if row_text.startswith("Eligible Branches"):
                break

            cols = row.locator(
                "xpath=.//div[contains(@class,'col-')][not(.//hr)][not(.//table)]"
            )

            texts = []

            col_count = await cols.count()

            for j in range(col_count):

                text = (await cols.nth(j).inner_text()).strip()

                texts.append(text)

            k = 0

            while k < len(texts):

                current = texts[k]

                if not current or current.startswith(":"):
                    k += 1
                    continue

                key = (
                    current.rstrip(":")
                    .lower()
                    .replace(" ", "_")
                    .replace("-", "_")
                    .replace("?", "")
                )

                value = ""

                if (
                    k + 1 < len(texts)
                    and texts[k + 1].startswith(":")
                ):
                    value = texts[k + 1][1:].strip()

                info[key] = value

                k += 1

        return info