from app.portal.portal import Portal
from app.orchestrator.company_orchestrator import CompanyOrchestrator


class PlacementAgent:

    def __init__(self):

        self.portal = Portal()

        self.company_orchestrator = CompanyOrchestrator()


    async def run(self):

        await self.portal.start()

        await self.portal.open_scheduled_companies()

        companies = await self.portal.get_companies()

        events = []

        for company in companies:

            status = self.company_orchestrator.save_company(company)

            events.append(
                {
                    "status": status,
                    "company": company
                }
            )

        await self.portal.stop()

        return events