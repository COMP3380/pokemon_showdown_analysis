from textual import on
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button, Label
from textual.containers import Container
from textual.screen import Screen
from textual.events import ScreenResume

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
        yield Label("", id="l1") 
        yield Footer()

    @on(ScreenResume)
    def on_screen_resume(self):
        l1 = self.query_one("#l1", Label)
        l1.update(f"Selected: {getattr(self.app, "period")}, {getattr(self.app, "metagame")}, {getattr(self.app, "cutoff")}") 

    def action_menu(self):
        self.app.switch_screen("menu")

    def action_back(self):
        self.app.pop_screen()
