from app.database.repository import CompanyRepository


class CompanyOrchestrator:

    def __init__(self):

        self.repository = CompanyRepository()

    def save_company(self, company: dict):

        company_info = company["full_details"]["company_information"]

        company_code = company_info["company_code"]

        if not self.repository.company_exists(company_code):

            self.repository.insert_company(company_info)

            return "NEW"

        stored = self.repository.get_company(company_code)

        tracked_fields = [
            "company_name",
            "company_type",
            "min_package",
            "max_package",
            "offering",
            "dead_backlog",
            "live_backlog",
            "year_down",
        ]

        for field in tracked_fields:

            current_value = (
                company_info["company"]
                if field == "company_name"
                else company_info[field]
            )

            if stored[field] != current_value:

                self.repository.update_company(company_info)

                return "UPDATED"

        return "EXISTING"