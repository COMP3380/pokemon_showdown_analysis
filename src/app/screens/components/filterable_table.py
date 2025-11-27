from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Input, DataTable
from textual.message import Message
from textual import on


class FilterableTable(Vertical):
    """
    A widget that displays an Input and a DataTable.
    Data is fetched by sending a message to the App to perform a query, which
    happens when the input bar is interacted with.
    """

    class FilterChanged(Message):
        """Custom message sent when the user types in the input."""

        def __init__(self, value: str) -> None:
            self.value = value
            super().__init__()

    def compose(self) -> ComposeResult:
        yield DataTable()
        yield Input(placeholder="Search by name...", id="search")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        # Set row cursor
        table.cursor_type = "row"

    @on(Input.Changed)
    def on_input_changed(self, event: Input.Changed) -> None:
        # Stop the event from bubbling up as a generic Input.Changed
        event.stop()
        # Send the custom message with the specific search value
        self.post_message(self.FilterChanged(event.value))

    def render_data(self, headers: list[str], rows: list[tuple]) -> None:
        """
        Public method to rebuild the table.
        Args:
            headers: A list of column names
            rows: A list of tuples containing the data
        """
        table = self.query_one(DataTable)
        table.clear(columns=True)
        table.add_columns(*headers)
        table.add_rows(rows)
