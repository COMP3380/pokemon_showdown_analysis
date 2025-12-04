from textual import on, events
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Static, DataTable
from textual.screen import Screen
from textual.events import ScreenResume
from .components.filterable_table import FilterableTable

class StatsP2(Screen):
    TITLE = "Stats"

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
        yield Static("", id="msg")
        yield FilterableTable(id="t1")
        yield Footer()

    @on(ScreenResume)
    def on_screen_resume(self):
        self.period = getattr(self.app, "period")
        self.metagame = getattr(self.app, "metagame")
        self.cutoff = getattr(self.app, "cutoff")
        l1 = self.query_one("#msg", Static)
        l1.update(f"Seeing usage stats for: Period: {self.period}, Metagame: {self.metagame}, Cutoff: {self.cutoff}")
        self.run_query("") # get initial data

    def on_mount(self):
        self.rows = []

    def action_menu(self):
        self.app.switch_screen("menu")

    def action_back(self):
        self.app.pop_screen()

    @on(FilterableTable.FilterChanged)
    def handle_db_filter(self, message: FilterableTable.FilterChanged):
        if message.id == "t1":
            self.run_query(message.value)

    def run_query(self, search_term: str = ""):
        sql = """
        SELECT Pokemon.id, Pokemon.name, pu.usage, rawCount, p95thGXE, p99thGXE, topGXE
        FROM PokemonUsage pu
        JOIN Pokemon ON Pokemon.id = pu.pokemon
        JOIN RawPokemonCount rpc ON rpc.pokemon = pu.pokemon
        AND rpc.metagame = pu.metagame
        AND rpc.period = pu.period
        WHERE pu.period = %s AND pu.metagame = %s AND pu.cutoff = %s
        AND Pokemon.name LIKE %s
        ORDER BY pu.usage DESC"""

        headers, self.rows = self.app.execute_query(sql, (self.period, self.metagame, self.cutoff, f"%{search_term}%",))
        widget = self.query_one(FilterableTable)
        widget.render_data(headers, self.rows)

    def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            self.log("Attempted submission")

            # Get the highlighted row in the highlighted table
            table = self.app.focused.parent
            data_table = table.query_one("#table", DataTable)
            row_index = data_table.cursor_row

            # Set the global variable to the selection and change pages
            if row_index is not None and len(self.rows) > 0:
                row = data_table.get_row_at(row_index)

                if table.id == "t1":
                    setattr(self.app, "stat_pokemon", row[0])
                    self.app.push_screen("pokemon_stats")
