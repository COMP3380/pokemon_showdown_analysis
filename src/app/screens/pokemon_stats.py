from textual import on, events
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Static, DataTable
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.events import ScreenResume
from .components.filterable_table import FilterableTable

class PokemonStats(Screen):
    TITLE = "Pokemon Stats"

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
        with VerticalScroll():
            yield Static("", id="msg")
            yield FilterableTable(id="ability_usage")
            yield FilterableTable(id="item_usage")
            yield FilterableTable(id="move_usage")
            yield FilterableTable(id="spread_usage")
            yield FilterableTable(id="tera_usage")
            yield FilterableTable(id="teammate_usage")
            yield FilterableTable(id="check_and_counter")
        yield Footer()

    @on(ScreenResume)
    def on_screen_resume(self):
        self.period = getattr(self.app, "period")
        self.metagame = getattr(self.app, "metagame")
        self.cutoff = getattr(self.app, "cutoff")
        self.pokemon = getattr(self.app, "stat_pokemon")
        l1 = self.query_one("#msg", Static)
        l1.update(f"""Seeing all usage stats for: Pokemon: {self.pokemon}, Period: {self.period}, Metagame: {self.metagame}, Cutoff: {self.cutoff}""")
        self.load_ability_usage("")
        self.load_item_usage("")
        self.load_move_usage("")
        self.load_spread_usage("")
        self.load_tera_usage("")
        self.load_teammate_usage("")
        self.load_check_and_counter("")

    def on_mount(self):
        self.rows = []

    def action_menu(self):
        self.app.switch_screen("menu")

    def action_back(self):
        self.app.pop_screen()

    @on(FilterableTable.FilterChanged)
    def handle_db_filter(self, message: FilterableTable.FilterChanged):
        if message.id == "ability_usage":
            self.load_ability_usage(message.value)
        elif message.id == "item_usage":
            self.load_item_usage(message.value)
        elif message.id == "move_usage":
            self.load_move_usage(message.value)
        elif message.id == "spread_usage":
            self.load_spread_usage(message.value)
        elif message.id == "tera_usage":
            self.load_tera_usage(message.value)
        elif message.id == "teammate_usage":
            self.load_teammate_usage(message.value)
        elif message.id == "check_and_counter":
            self.load_check_and_counter(message.value)

    def load_ability_usage(self, search_term: str = ""):
        sql = """
        SELECT Ability.name as 'Ability Name', usage
        FROM Ability
        JOIN AbilityUsage ab ON ab.ability = Ability.id
        JOIN PokemonHasAbility pha ON pha.pokemon = ab.pokemon AND pha.ability = ab.ability
        JOIN Pokemon ON Pokemon.id = pha.pokemon
        WHERE period = %s AND metagame = %s AND cutoff = %s AND Pokemon.id = %s AND Ability.name LIKE %s
        ORDER BY usage DESC"""
        headers, self.rows = self.app.execute_query(sql, (self.period, self.metagame, self.cutoff, self.pokemon, f"%{search_term}%"))
        widget = self.query_one("#ability_usage", FilterableTable)
        widget.render_data(headers, self.rows)

    def load_item_usage(self, search_term: str = ""):
        sql = """
        SELECT Item.name as 'Item Name', usage
        FROM Item
        JOIN ItemUsage ON ItemUsage.item = Item.id
        JOIN Pokemon ON Pokemon.id = ItemUsage.pokemon
        WHERE period = %s AND metagame = %s AND cutoff = %s AND Pokemon.id = %s AND Item.name LIKE %s
        ORDER BY usage DESC"""
        headers, self.rows = self.app.execute_query(sql, (self.period, self.metagame, self.cutoff, self.pokemon, f"%{search_term}%"))
        widget = self.query_one("#item_usage", FilterableTable)
        widget.render_data(headers, self.rows)

    def load_move_usage(self, search_term: str = ""):
        sql = """
        SELECT Move.name as 'Move Name', usage
        FROM Move
        JOIN MoveUsage ON MoveUsage.move = Move.id
        JOIN Pokemon ON Pokemon.id = MoveUsage.pokemon
        WHERE period = %s AND metagame = %s AND cutoff = %s AND Pokemon.id = %s AND Move.name LIKE %s
        ORDER BY usage DESC"""
        headers, self.rows = self.app.execute_query(sql, (self.period, self.metagame, self.cutoff, self.pokemon, f"%{search_term}%"))
        widget = self.query_one("#move_usage", FilterableTable)
        widget.render_data(headers, self.rows)

    def load_spread_usage(self, search_term: str = ""):
        sql = """
        SELECT spread, usage
        FROM SpreadUsage
        WHERE period = %s AND metagame = %s AND cutoff = %s AND pokemon = %s AND spread LIKE %s
        ORDER BY usage DESC"""
        headers, self.rows = self.app.execute_query(sql, (self.period, self.metagame, self.cutoff, self.pokemon, f"%{search_term}%"))
        widget = self.query_one("#spread_usage", FilterableTable)
        widget.render_data(headers, self.rows)

    def load_tera_usage(self, search_term: str = ""):
        sql = """
        SELECT type as 'Tera Type', usage
        FROM TeraUsage
        JOIN Pokemon ON Pokemon.id = TeraUsage.pokemon
        WHERE period = %s AND metagame = %s AND cutoff = %s AND Pokemon.id = %s AND type LIKE %s
        ORDER BY usage DESC"""
        headers, self.rows = self.app.execute_query(sql, (self.period, self.metagame, self.cutoff, self.pokemon, f"%{search_term}%"))
        widget = self.query_one("#tera_usage", FilterableTable)
        widget.render_data(headers, self.rows)

    def load_teammate_usage(self, search_term: str = ""):
        sql = """
        SELECT out_p.name as 'Teammate Name', usage
        FROM TeammateUsage
        JOIN Pokemon out_p ON out_p.id = TeammateUsage.pokemonTeammate
        JOIN Pokemon curr_p ON curr_p.id = TeammateUsage.pokemonCurrent
        WHERE period = %s AND metagame = %s AND cutoff = %s AND curr_p.id = %s AND out_p.name LIKE %s
        ORDER BY usage DESC"""
        headers, self.rows = self.app.execute_query(sql, (self.period, self.metagame, self.cutoff, self.pokemon, f"%{search_term}%"))
        widget = self.query_one("#teammate_usage", FilterableTable)
        widget.render_data(headers, self.rows)

    def load_check_and_counter(self, search_term: str = ""):
        sql = """
        SELECT out_p.name as 'Opponent Name', koRate, switchRate, occurrence
        FROM CheckAndCounter
        JOIN Pokemon out_p ON out_p.id = CheckAndCounter.pokemonOpposing
        JOIN Pokemon curr_p ON curr_p.id = CheckAndCounter.pokemonCurrent
        WHERE period = %s AND metagame = %s AND cutoff = %s AND curr_p.id = %s AND out_p.name LIKE %s
        ORDER BY koRate DESC, switchRate DESC"""
        headers, self.rows = self.app.execute_query(sql, (self.period, self.metagame, self.cutoff, self.pokemon, f"%{search_term}%"))
        widget = self.query_one("#check_and_counter", FilterableTable)
        widget.render_data(headers, self.rows)
