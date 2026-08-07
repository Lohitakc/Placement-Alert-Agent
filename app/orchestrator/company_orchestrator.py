from app.database.repository import CompanyRepository


class CompanyOrchestrator:

    def __init__(self):

        self.repository = CompanyRepository()

    def save_company(self, company: dict):

        company_info = company["full_details"]["company_information"]

        company_code = company_info["company_code"]

        if self.repository.company_exists(company_code):

            return False

        self.repository.insert_company(company_info)

        return True