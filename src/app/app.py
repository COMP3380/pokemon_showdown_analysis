import pymssql
from textual.app import App
from screens.menu import Menu
from screens.moves import Moves
from screens.pokemon import Pokemon
from screens.items import Items
from screens.items_p2 import ItemsP2
from screens.abilities import Abilities
from screens.typechart import Typechart
from screens.stats import Stats
from screens.queries import Queries

class PokiTUI(App):
    # List of pages/screens that our app will use
    SCREENS = {
        "menu": Menu,
        "moves": Moves,
        "pokemon": Pokemon,
        "items": Items,
        "items_p2": ItemsP2,
        "abilities": Abilities,
        "typechart": Typechart,
        "stats": Stats,
        "queries": Queries,
    }

    def on_startup(self) -> None:
        pass

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

        # Set any variables
        self.item = ""

        # Start at menu screen
        self.push_screen("menu")

if __name__ == "__main__":
    PokiTUI().run()
