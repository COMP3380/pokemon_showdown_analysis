from textual import on, events
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Static, DataTable
from textual.screen import Screen
from textual.events import ScreenResume
from .components.filterable_table import FilterableTable

class PokemonP2(Screen):
    TITLE = "Pokemon"

    BINDINGS = [
        ("Ctrl-q", "quit", "Quit"),
        ("m", "menu", "Menu"),
        ("b", "back", "Back"),
    ]

    DEFAULT_CSS = """
    #msg {
      margin: 2;
    }
    #msg2 {
      margin: 2;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("", id="msg")
        yield FilterableTable(id="abilities_table")
        yield Static("", id="msg2")
        yield FilterableTable(id="moves_table")
        yield Footer()

    @on(ScreenResume)
    def on_screen_resume(self):
        self.pokemon = getattr(self.app, "pokemon")
        l1 = self.query_one("#msg", Static)
        l1.update(f"Seeing Abilities for: {self.pokemon}")
        l2 = self.query_one("#msg2", Static)
        l2.update(f"Seeing Moves for: {self.pokemon}")
        self.load_abilities("") # get initial data
        self.load_moves("") # get initial data

    def on_mount(self):
        self.cursor = getattr(self.app, "cursor") # get the DB connection
        self.rows = []

    def action_menu(self):
        self.app.switch_screen("menu")

    def action_back(self):
        self.app.pop_screen()

    @on(FilterableTable.FilterChanged)
    def handle_db_filter(self, message: FilterableTable.FilterChanged):
        if message.id == "abilities_table":
            self.load_abilities(message.value)
        elif message.id == "moves_table":
            self.load_moves(message.value)

    def load_abilities(self, search_term: str):
        if not self.cursor:
            return

        if search_term:
            sql = """
            SELECT id, name FROM Ability a
            JOIN PokemonHasAbility pa ON pa.ability = a.id
            WHERE pa.pokemon = %s AND a.name LIKE %s"""
            self.cursor.execute(sql, (self.pokemon, f"%{search_term}%",))
        else:
            sql = """
            SELECT id, name FROM Ability a
            JOIN PokemonHasAbility pa ON pa.ability = a.id
            WHERE pa.pokemon = %s"""
            self.cursor.execute(sql, (self.pokemon,))

        self.rows = self.cursor.fetchall()
        headers = [desc[0] for desc in self.cursor.description]

        widget = self.query_one("#abilities_table", FilterableTable)
        widget.render_data(headers, self.rows)

    def load_moves(self, search_term: str):
        if not self.cursor:
            return

        if search_term:
            sql = """
            SELECT id, name, type, power, category, pp, accuracy FROM Move m
            JOIN PokemonLearnsMove pm ON pm.move = m.id
            WHERE pm.pokemon = %s AND m.name LIKE %s"""
            self.cursor.execute(sql, (self.pokemon, f"%{search_term}%",))
        else:
            sql = """
            SELECT id, name, type, power, category, pp, accuracy FROM Move m
            JOIN PokemonLearnsMove pm ON pm.move = m.id
            WHERE pm.pokemon = %s"""
            self.cursor.execute(sql, (self.pokemon,))

        self.rows = self.cursor.fetchall()
        headers = [desc[0] for desc in self.cursor.description]

        widget = self.query_one("#moves_table", FilterableTable)
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

                if table.id == "abilities_table":
                    setattr(self.app, "ability", row[0])
                    self.app.push_screen("abilities_p2")
                elif table.id == "moves_table":
                    setattr(self.app, "move", row[0])
                    self.app.push_screen("moves_p2")
