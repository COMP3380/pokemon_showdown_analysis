from textual import on, events
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Static, DataTable
from textual.screen import Screen
from textual.events import ScreenResume
from .components.filterable_table import FilterableTable

class AbilitiesP2(Screen):
    TITLE = "Abilities"

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
        yield FilterableTable()
        yield Footer()

    @on(ScreenResume)
    def on_screen_resume(self):
        self.ability = getattr(self.app, "ability")
        l1 = self.query_one("#msg", Static)
        l1.update(f"Seeing pokemon that have: {self.ability}")
        self.run_query("") # get initial data

    def on_mount(self):
        self.cursor = getattr(self.app, "cursor") # get the DB connection
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
        """
        Connects to DB, gets results, and pushes them into the widget
        """
        if not self.cursor:
            return

        if search_term:
            sql = """
            SELECT id, name, type1, type2, hp, attack, defense, spattack, spdefense, speed, tier 
            FROM Pokemon p
            JOIN PokemonHasAbility pa ON pa.pokemon = p.id
            WHERE pa.ability = %s AND p.name LIKE %s"""
            self.cursor.execute(sql, (self.ability, f"%{search_term}%",))
        else:
            sql = """
            SELECT id, name, type1, type2, hp, attack, defense, spattack, spdefense, speed, tier 
            FROM Pokemon p
            JOIN PokemonHasAbility pa ON pa.pokemon = p.id
            WHERE pa.ability = %s"""
            self.cursor.execute(sql, (self.ability,))

        self.rows = self.cursor.fetchall()
        headers = [desc[0] for desc in self.cursor.description]

        widget = self.query_one(FilterableTable)
        widget.render_data(headers, self.rows)

    def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            self.log("Attempted submission")

            # Get the highlighted row in the table
            table = self.query_one(FilterableTable)
            data_table = table.query_one("#table", DataTable)
            row_index = data_table.cursor_row

            # Set the global variable to the selection and change pages
            if row_index is not None and len(self.rows) > 0:
                row = data_table.get_row_at(row_index)
                setattr(self.app, "pokemon", row[0])

                self.app.push_screen("pokemon_p2")
