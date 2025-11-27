from textual.app import App, ComposeResult
from textual import on

from screens.components.filterable_table import FilterableTable


class Database:
    """Simulates a database connection."""

    def __init__(self) -> None:
        self._headers: list[str] = ["ID", "Product Name", "Price", "Category"]
        self._data: list[tuple] = [
            (1, "Laptop", 999.99, "Electronics"),
            (2, "Coffee Mug", 12.50, "Kitchen"),
            (3, "Mouse", 25.00, "Electronics"),
            (4, "Desk Lamp", 45.00, "Furniture"),
            (5, "Monitor", 150.00, "Electronics")
        ]

    def query(self, search_term: str | None) -> tuple[list[str], list[tuple]]:
        """Simulates: SELECT * FROM table WHERE name LIKE %search_term%"""
        headers: list[str] = self._headers
        rows: list[tuple]

        if search_term is not None:
            rows = [
                r for r in self._data
                if search_term.lower() in r[1].lower()
            ]
        else:
            rows = self._data

        return headers, rows


class Test(App):
    def __init__(self) -> None:
        super().__init__()
        self.db = Database()

    def compose(self) -> ComposeResult:
        yield FilterableTable()

    def on_mount(self) -> None:
        """Load initial data when app starts."""
        self.run_query("")

    @on(FilterableTable.FilterChanged)
    def handle_db_filter(self, message: FilterableTable.FilterChanged):
        """This captures the custom message from the widget."""
        self.run_query(message.value)

    def run_query(self, search_term: str):
        """
        Connects to DB, gets results, and pushes them into the widget
        """
        headers, rows = self.db.query(search_term)

        widget = self.query_one(FilterableTable)
        widget.render_data(headers, rows)


if __name__ == "__main__":
    app = Test()
    app.run()
