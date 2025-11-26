from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button
from textual.containers import Container
from textual.screen import Screen

class Items(Screen):
    TITLE = "Items"
    CSS_PATH = "styles/items.tcss"

    BINDINGS = [
        ("Ctrl-q", "quit", "Quit"),
        ("m", "menu", "Menu"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    def action_menu(self):
        self.app.switch_screen("menu")

