import asyncio
from rich import print
from app.portal.portal import Portal
from app.database.models import create_tables
from app.orchestrator.company_orchestrator import CompanyOrchestrator
from app.orchestrator.monitor import Monitor


async def main():

    create_tables()

    orchestrator = CompanyOrchestrator()

    monitor = Monitor(interval_minutes=60)

    try:

        while True:

            portal = Portal()

            try:

                await portal.start()

                await portal.open_scheduled_companies()

                companies = await portal.get_companies()

                print()

                print(f"Found {len(companies)} companies\n")

                for company in companies:

                    status = orchestrator.save_company(company)

                    if status == "NEW":
                        print(f"🟢 NEW: {company['company_name']}")

                    elif status == "UPDATED":
                        print(f"🟡 UPDATED: {company['company_name']}")

                    else:
                        print(f"⚪ EXISTING: {company['company_name']}")

                print("-" * 80)

            finally:

                await portal.stop()

            await monitor.sleep()

    except (KeyboardInterrupt, asyncio.CancelledError):

        print("\nAgent stopped by user.")


if __name__ == "__main__":
    asyncio.run(main())