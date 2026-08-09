from app.database.repository import CompanyRepository

repo = CompanyRepository()

company = repo.get_company("COZ2026-271")

print("Before:")
print(company)

updated_company = {
    "company_code": "COZ2026-271",
    "company": "Cognizant",
    "company_type": "Regular",
    "min_package": "99",          # <-- Temporary change
    "max_package": "99",         # <-- Temporary change
    "offering": "Placement",
    "dead_backlog": "Allowed",
    "live_backlog": "Not Allowed",
    "year_down": "Allowed",
}

repo.update_company(updated_company)

print("\nAfter:")
print(repo.get_company("COZ2026-271"))