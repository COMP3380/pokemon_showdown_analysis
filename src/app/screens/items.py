from textual import on, events
from textual.app import ComposeResult
from textual.widgets import Header, Footer, DataTable, Static
from textual.screen import Screen
from .components.filterable_table import FilterableTable

class Items(Screen):
    TITLE = "Items"
    CSS_PATH = "styles/items.tcss"

    BINDINGS = [
        ("Ctrl-q", "quit", "Quit"),
        ("m", "menu", "Menu"),
        ("b", "back", "Back"),
    ]

    DEFAULT_CSS = """
    #msg {
      margin: 2;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Search for your desired Item!", id="msg")
        yield FilterableTable()
        yield Footer()

    def on_mount(self):
        self.run_query("") # get initial data
        self.rows = []

    def action_menu(self):
        self.app.switch_screen("menu")

    def action_back(self):
        self.app.pop_screen()

    @on(FilterableTable.FilterChanged)
    def handle_db_filter(self, message: FilterableTable.FilterChanged):
        """This captures the custom message from the widget."""
        self.run_query(message.value)

    def run_query(self, search_term: str):
        sql = "SELECT id, name FROM Item WHERE name LIKE %s"

        headers, self.rows = self.app.execute_query(sql, (f"%{search_term}%",))
        widget = self.query_one(FilterableTable)
        widget.render_data(headers, self.rows)
