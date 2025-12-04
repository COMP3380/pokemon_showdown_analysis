import pymssql
from textual.app import App
from screens.menu import Menu
from screens.moves import Moves
from screens.moves_p2 import MovesP2
from screens.pokemon import Pokemon
from screens.pokemon_p2 import PokemonP2
from screens.items import Items
from screens.items_p2 import ItemsP2
from screens.abilities import Abilities
from screens.abilities_p2 import AbilitiesP2
from screens.typechart import Typechart
from screens.stats import Stats
from screens.stats_p2 import StatsP2
from screens.queries import Queries

class PokiTUI(App):
    # List of pages/screens that our app will use
    SCREENS = {
        "menu": Menu,
        "moves": Moves,
        "moves_p2": MovesP2,
        "pokemon": Pokemon,
        "pokemon_p2": PokemonP2,
        "items": Items,
        "items_p2": ItemsP2,
        "abilities": Abilities,
        "abilities_p2": AbilitiesP2,
        "typechart": Typechart,
        "stats": Stats,
        "stats_p2": StatsP2,
        "queries": Queries,
    }


    # On startup, show the user the Menu
    def on_mount(self):
        # Create DB connection 
        self.conn = pymssql.connect(
            server="uranium.cs.umanitoba.ca",
            user="vuqh1",
            password="7990597",
            database="cs3380",
        )
        self.cursor = self.conn.cursor()

        # Variables for basic pages
        self.item = ""
        self.ability = ""
        self.move = ""
        self.pokemon = ""
        
        # Variables for stats page
        self.period = ""
        self.metagame = ""
        self.cutoff = ""

        # Start at menu screen
        self.push_screen("menu")

if __name__ == "__main__":
    PokiTUI().run()
