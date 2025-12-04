from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Input, DataTable
from textual.message import Message
from textual.binding import Binding
from textual import on


class FilterableTable(Vertical):
    """
    A widget that displays an Input and a DataTable.
    Data is fetched by sending a message to the App to perform a query, which
    happens when the input bar is interacted with.
    """

    DEFAULT_CSS = """
    FilterableTable {
        max-height: 48;
    }

    FilterableTable > DataTable {
        height: 1fr;
    }

    FilterableTable > Input {
        dock: bottom;
    }
    """

    BINDINGS = [
        Binding("j", "cursor_down", "Move down 1 row", show=False),
        Binding("k", "cursor_up", "Move up 1 row", show=False),
        Binding("ctrl+d", "page_down", "Move down 1 page", show=False),
        Binding("ctrl+u", "page_up", "Move up 1 page", show=False),
        Binding("G", "bottom", "Go to bottom", show=False),
        Binding("g", "top", "Go to top", show=False),
    ]

    class FilterChanged(Message):
        """Custom message sent when the user types in the input."""

        def __init__(self, the_id, value: str) -> None:
            super().__init__()
            self.value = value
            self.id = the_id

    def compose(self) -> ComposeResult:
        yield DataTable(id="table")
        yield Input(placeholder="Search by name...", id="search")

    def on_mount(self) -> None:
        self.table = self.query_one("#table", DataTable)
        self.table.cursor_type = "row"

    @on(Input.Changed)
    def on_input_changed(self, event: Input.Changed) -> None:
        # Stop the event from bubbling up as a generic Input.Changed
        event.stop()
        # Send the custom message with the specific search value
        self.post_message(self.FilterChanged(self.id, event.value))

    def render_data(self, headers: list[str], rows: list[tuple]) -> None:
        """
        Public method to rebuild the table.
        Args:
            headers: A list of column names
            rows: A list of tuples containing the data
        """
        self.table.clear(columns=True)
        self.table.add_columns(*headers)
        self.table.add_rows(rows)

    def action_cursor_down(self):
        self.table.action_cursor_down()

    def action_cursor_up(self):
        self.table.action_cursor_up()

    def action_page_down(self):
        self.table.action_page_down()

    def action_page_up(self):
        self.table.action_page_up()

    def action_bottom(self):
        self.table.action_scroll_bottom()

    def action_top(self):
        self.table.action_scroll_top()
