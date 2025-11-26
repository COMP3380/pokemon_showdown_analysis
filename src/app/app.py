from textual.app import App
from screens.menu import Menu
from screens.moves import Moves
from screens.pokemon import Pokemon
from screens.items import Items
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
        "abilities": Abilities,
        "typechart": Typechart,
        "stats": Stats,
        "queries": Queries,
    }

    # On startup, show the user the Menu
    def on_mount(self):
        self.push_screen("menu")

if __name__ == "__main__":
    PokiTUI().run()
