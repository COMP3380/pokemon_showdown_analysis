from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button, Label
from textual.containers import Container
from textual.screen import Screen

# Second Page for Stats Section
class StatsP2(Screen):
    TITLE = "Stats"
    CSS_PATH = "styles/stats_p2.tcss"

    BINDINGS = [
        ("Ctrl-q", "quit", "Quit"),
        ("m", "menu", "Menu"),
        ("b", "back", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Nothing here yet...")
        yield Footer()

    def action_menu(self):
        self.app.switch_screen("menu")

    def action_back(self):
        self.app.pop_screen()
