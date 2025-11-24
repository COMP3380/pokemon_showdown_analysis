from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button
from textual.containers import Container
from textual.screen import Screen

class Abilities(Screen):
    TITLE = "Abilities"
    CSS_PATH = "styles/abilities.tcss"

    BINDINGS = [
        ("Ctrl-q", "quit", "Quit"),
        ("m", "menu", "Menu"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    def action_menu(self):
        self.app.switch_screen("menu")

