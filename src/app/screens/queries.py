from textual import on
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button
from textual.containers import Container
from textual.screen import Screen

class Queries(Screen):
    TITLE = "Queries & Analysis"
    CSS_PATH = "styles/queries.tcss"

    BINDINGS = [
        ("Ctrl-q", "quit", "Quit"),
        ("m", "menu", "Menu"),
        ("1", "q1", "Base..."),
        ("2", "q2", "Highest..."),
        ("3", "q3", "Stat..."),
        ("4", "q4", "Underrated..."),
        ("5", "q5", "Best.."),
        ("6", "q6", "Diverse.."),
        ("7", "q7", "Noob.."),
        ("8", "q8", "Effectiveness..."),
    ]

    def action_menu(self):
        self.app.switch_screen("menu")

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="queries_screen"):
            yield Button("1 - Base Stats Priority", id="q1")
            yield Button("2 - Highest Usage", id="q2")
            yield Button("3 - Stat Viability", id="q3")
            yield Button("4 - Underrated Abilities", id="q4")
            yield Button("5 - Best Pairs", id="q5")
            yield Button("6 - Diverse Movesets", id="q6")
            yield Button("7 - Noob Pokemon", id="q7")
            yield Button("8 - Effectiveness/Counter", id="q8")
        yield Footer()

    @on(Button.Pressed, "#q1")
    def action_q1(self): self.app.push_screen("q1")
    @on(Button.Pressed, "#q2")
    def action_q2(self): self.app.push_screen("q2")
    @on(Button.Pressed, "#q3")
    def action_q3(self): self.app.push_screen("q3")
    @on(Button.Pressed, "#q4")
    def action_q4(self): self.app.push_screen("q4")
    @on(Button.Pressed, "#q5")
    def action_q5(self): self.app.push_screen("q5")
    @on(Button.Pressed, "#q6")
    def action_q6(self): self.app.push_screen("q6")
    @on(Button.Pressed, "#q7")
    def action_q7(self): self.app.push_screen("q7")
    @on(Button.Pressed, "#q8")
    def action_q8(self): self.app.push_screen("q8")


