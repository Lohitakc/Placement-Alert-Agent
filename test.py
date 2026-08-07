from app.database.models import create_tables
from app.database.repository import CompanyRepository

create_tables()

repo = CompanyRepository()

company = {
    "company_code": "TEST001",
    "company": "Test Company",
    "company_type": "Placement",
    "min_package": "10",
    "max_package": "20",
    "offering": "Placement",
    "dead_backlog": "Allowed",
    "live_backlog": "Not Allowed",
    "year_down": "Allowed",
}

print(repo.company_exists("TEST001"))

repo.insert_company(company)

print(repo.company_exists("TEST001"))