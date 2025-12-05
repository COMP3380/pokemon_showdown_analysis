import pymssql
from textual.app import App
from screens.menu import Menu
from screens.moves import Moves
from screens.moves_p2 import MovesP2
from screens.pokemon import Pokemon
from screens.pokemon_p2 import PokemonP2
from screens.items import Items
from screens.abilities import Abilities
from screens.abilities_p2 import AbilitiesP2
from screens.typechart import Typechart
from screens.stats import Stats
from screens.stats_p2 import StatsP2
from screens.queries import Queries
from screens.pokemon_stats import PokemonStats
from screens.q1 import Q1, Q1Results
from screens.q2 import Q2, Q2Results


class PokiTUI(App):
    # List of pages/screens that our app will use
    SCREENS = {
        "menu": Menu,
        "moves": Moves,
        "moves_p2": MovesP2,
        "pokemon": Pokemon,
        "pokemon_p2": PokemonP2,
        "items": Items,
        "abilities": Abilities,
        "abilities_p2": AbilitiesP2,
        "typechart": Typechart,
        "stats": Stats,
        "stats_p2": StatsP2,
        "queries": Queries,
        "pokemon_stats": PokemonStats,
        "q1": Q1,
        "q1_results": Q1Results,
        "q2": Q2,
        "q2_results": Q2Results
    }

    # On startup, show the user the Menu

    def on_mount(self):
        self.connect_db()

        # Variables for basic pages
        self.item = ""
        self.ability = ""
        self.move = ""
        self.pokemon = ""

        # Variables for stats page
        self.period = ""
        self.metagame = ""
        self.cutoff = ""
        self.stat_pokemon = ""

        # Start at menu screen
        self.push_screen("menu")

    def connect_db(self):
        # Create DB connection
        self.conn = pymssql.connect(
            server="uranium.cs.umanitoba.ca",
            user="vuqh1",
            password="7990597",
            database="cs3380",
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, sql: str, params: tuple = ()):
        if self.cursor is None:
            self.connect_db()

        try:
            self.cursor.execute(sql, params)
        except pymssql.OperationalError:
            # Connection probably dead, reconnect
            self.connect_db()
            self.cursor.execute(sql, params)

        rows = self.cursor.fetchall()
        headers = [desc[0] for desc in self.cursor.description]
        return headers, rows


if __name__ == "__main__":
    PokiTUI().run()
