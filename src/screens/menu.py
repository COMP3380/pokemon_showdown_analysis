from textual import on
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button, Static
from textual.containers import Container
from textual.screen import Screen
from textual.geometry import Offset

from .components.confirmation_dialog import ConfirmationDialog
from setup.process_sql import generate_and_execute_sql, 

class Menu(Screen):
    TITLE = "Menu"
    CSS_PATH = "styles/menu.tcss"

    BINDINGS = [
        ("Ctrl-q", "quit", "Quit"),
        ("m", "moves", "Moves"),
        ("p", "pokemon", "Pokemon"),
        ("i", "items", "Items"),
        ("a", "abilities", "Abilities"),
        ("t", "typechart", "Typechart"),
        ("s", "stats", "Stats"),
        ("q", "queries", "Queries & Analysis"),
        ("r", "repopulate", "Repopulate"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="menu_screen"):
            yield Button("Moves", id="moves")
            yield Button("Pokemon", id="pokemon")
            yield Button("Items", id="items")
            yield Button("Abilities", id="abilities")
            yield Button("Typechart", id="typechart")
            yield Button("Stats", id="stats")
            yield Button("Queries & Analysis", id="queries")
            yield Button("Repopulate", id="repopulate")
        yield Footer()

    @on(Button.Pressed, "#moves")
    def action_moves(self): self.app.push_screen("moves")
    @on(Button.Pressed, "#pokemon")
    def action_pokemon(self): self.app.push_screen("pokemon")
    @on(Button.Pressed, "#items")
    def action_items(self): self.app.push_screen("items")
    @on(Button.Pressed, "#abilities")
    def action_abilities(self): self.app.push_screen("abilities")
    @on(Button.Pressed, "#typechart")
    def action_typechart(self): self.app.push_screen("typechart")
    @on(Button.Pressed, "#stats")
    def action_stats(self): self.app.push_screen("stats")
    @on(Button.Pressed, "#queries")
    def action_queries(self): self.app.push_screen("queries")

    @on(Button.Pressed, "#repopulate")
    def action_repopulate(self): 
        self.log("Repopulate selected")
        conf_dialog = ConfirmationDialog()
        self.mount(conf_dialog)
        parent_width, parent_height = self.size.width, self.size.height
        dialog_width, dialog_height = conf_dialog.styles.width.value, conf_dialog.styles.height.value
        conf_dialog.styles.offset = Offset(
            (parent_width - dialog_width) // 2,
            (parent_height - dialog_height) // 2
        )
        conf_dialog.focus()

    def on_confirmation_dialog_yes(self, msg: ConfirmationDialog.Yes):
        self.log("Confirmed choice")
        generate_sql.main()

    def on_confirmation_dialog_no(self, msg: ConfirmationDialog.No):
        self.log("Retracted choice")
        pass

