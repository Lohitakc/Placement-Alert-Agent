from app.database.database import get_connection


class CompanyRepository:

    def company_exists(self, company_code: str) -> bool:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM companies
            WHERE company_code = ?
            """,
            (company_code,)
        )

        exists = cursor.fetchone() is not None

        connection.close()

        return exists


    def insert_company(self, company: dict):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO companies
            (
                company_code,
                company_name,
                company_type,
                min_package,
                max_package,
                offering,
                dead_backlog,
                live_backlog,
                year_down
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                company["company_code"],
                company["company"],
                company["company_type"],
                company["min_package"],
                company["max_package"],
                company["offering"],
                company["dead_backlog"],
                company["live_backlog"],
                company["year_down"],
            )
        )

        connection.commit()

        connection.close()