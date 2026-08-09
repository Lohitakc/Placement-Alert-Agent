import asyncio
from rich import print
from app.portal.portal import Portal
from app.database.models import create_tables
from app.orchestrator.company_orchestrator import CompanyOrchestrator
from app.orchestrator.monitor import Monitor
from app.notifications.notifier import Notifier


async def main():

    create_tables()

    orchestrator = CompanyOrchestrator()
    notifier = Notifier()

    monitor = Monitor(interval_minutes=1)

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

                    info = company["full_details"]["company_information"]

                    result = orchestrator.save_company(company)

                    status = result["status"]
                    changes = result["changes"]

                    if status == "NEW":

                        print(f"🟢 NEW: {company['company_name']}")

                        notifier.send(
                            "🟢 New Company",
                            f"{company['company_name']}\n"
                            f"Package: {info['min_package']} - {info['max_package']} LPA"
                        )

                    elif status == "UPDATED":

                        print(f"🟡 UPDATED: {company['company_name']}")

                        change_lines = []

                        for field, change in changes.items():

                            field_name = field.replace("_", " ").title()

                            change_lines.append(
                                f"{field_name}: {change['old']} → {change['new']}"
                            )

                        message = (
                            f"{company['company_name']}\n\n"
                            + "\n".join(change_lines)
                        )

                        notifier.send(
                            "🟡 Company Updated",
                            message
                        )

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