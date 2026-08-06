import asyncio
from rich import print
from app.portal.portal import Portal


async def main():

    portal = Portal()

    await portal.start()

    await portal.open_scheduled_companies()

    companies = await portal.get_companies()

    print()

    print(f"Found {len(companies)} companies\n")

    for company in companies:

        print("Company Information")
        print(company["full_details"]["company_information"])

        print("\nAttachments")
        print(company["full_details"]["attachments"])

        print("-" * 80)

    input()

    await portal.stop()


if __name__ == "__main__":
    asyncio.run(main())