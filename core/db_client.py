import sqlite3
import allure


class DatabaseClient:
    def __init__(self, db_path: str = "test.db"):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        return self

    def close(self):
        if self.connection:
            self.connection.close()

    def _log_to_allure(self, query: str, params: tuple):
        """Helper method to attach SQL query details to Allure report."""
        clean_query = " ".join(query.split())
        with allure.step(f"SQL: {clean_query}"):
            allure.attach(
                f"Query:\n{query.strip()}\n\nParameters:\n{params}",
                name="SQL Execution Details",
                attachment_type=allure.attachment_type.TEXT
            )

    def execute(self, query: str, params: tuple = ()):
        self._log_to_allure(query, params)
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor

    def fetch_one(self, query: str, params: tuple = ()):
        self._log_to_allure(query, params)
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None

    def fetch_all(self, query: str, params: tuple = ()):
        self._log_to_allure(query, params)
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]