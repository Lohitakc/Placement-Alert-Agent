import asyncio
from rich import print
from app.portal.portal import Portal
from app.database.models import create_tables
from app.orchestrator.company_orchestrator import CompanyOrchestrator


async def main():

    create_tables()

    orchestrator = CompanyOrchestrator()

    portal = Portal()

    await portal.start()

    await portal.open_scheduled_companies()

    companies = await portal.get_companies()

    print()

    print(f"Found {len(companies)} companies\n")

    for company in companies:

        print(f"Processing: {company['company_name']}")

        is_new = orchestrator.save_company(company)

        print("save_company() returned:", is_new)

        if is_new:
            print(f"🟢 NEW: {company['company_name']}")
        else:
            print(f"⚪ Existing: {company['company_name']}")

    print("-" * 80)

    await portal.stop()


if __name__ == "__main__":
    asyncio.run(main())