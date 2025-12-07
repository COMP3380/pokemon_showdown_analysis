from textual import on
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Label, OptionList
from textual.containers import Horizontal, Container
from textual.widgets.option_list import Option
from textual.screen import Screen
from textual.binding import Binding
from .components.vim_option_list import VimOptionList


class Typechart(Screen):
    TITLE = "Typechart"
    CSS_PATH = "styles/typechart.tcss"

    BINDINGS = [
        ("Ctrl-q", "quit", "Quit"),
        ("m", "menu", "Menu"),
        ("b", "back", "Back"),
        Binding("h,left", "prevlist", "Previous OptionList", show=False),
    ]

    TYPES = [
        "Normal","Fire","Water","Electric","Grass","Ice","Fighting","Poison","Ground",
        "Flying","Psychic","Bug","Rock","Ghost","Dragon","Dark","Steel","Fairy"
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Select Attacking Type → Then Select Defending Type!", id="l1")

        with Horizontal():
            yield VimOptionList(
                *[Option(t, id=t.lower()) for t in self.TYPES],
                id="attack"
            )

            yield VimOptionList(
                *[Option(t, id=t.lower()) for t in self.TYPES],
                id="defend",
            )

        # Big result output area
        yield Container(
            Label("", id="result_msg"),
            id="result_container",
        )

        yield Footer()

    def on_mount(self):
        df = self.query_one("#defend", OptionList)
        df.disabled = True

    def action_menu(self):
        self.swap_lists("defend", "attack")
        self.app.switch_screen("menu")

    def action_back(self):
        self.swap_lists("defend", "attack")
        self.app.pop_screen()

    def action_prevlist(self):
        atk = self.query_one("#attack", OptionList)
        df = self.query_one("#defend", OptionList)
        if not df.disabled:
            atk.disabled = False
            df.disabled = True
            atk.focus() 


    @on(OptionList.OptionSelected)
    def on_select(self, event: OptionList.OptionSelected):

        # Attack Type chosen
        if event.option_list.id == "attack":
            setattr(self.app, "attack_type", event.option.id)
            self.swap_lists("attack", "defend")
            return

        # Defense Type chosen
        if event.option_list.id == "defend":
            setattr(self.app, "defend_type", event.option.id)
            self.show_effectiveness_message()


    def show_effectiveness_message(self):
        attack = self.app.attack_type
        defend = self.app.defend_type

        sql = """
            SELECT effectiveness
            FROM TypeEffectiveness
            WHERE attackingType = %s AND defendingType = %s
        """

        try:
            headers, rows = self.app.execute_query(sql, (attack, defend))
            if not rows:
                msg = "No data found for this matchup."
            else:
                value = int(rows[0][0])
                msg = self.effectiveness_text(value)

        except Exception as e:
            msg = f"Query Error: {e}"

        formatted = f"{attack.title()} → {defend.title()} : {msg}"
        result_label = self.query_one("#result_msg", Label)
        result_label.update(formatted)

        # After showing the result, switch back to picking attacking type
        atk = self.query_one("#attack", OptionList)
        df = self.query_one("#defend", OptionList)
        atk.disabled = False
        df.disabled = True

    def effectiveness_text(self, value: int) -> str:
        return {
            1: "Super Effective! (2x Damage)",
            0: "It's effective. (1x Damage)",
            2: "Not Very Effective... (½x Damage)",
            3: "It doesn't affect the target! (0x Damage)",
        }.get(value, "Unknown Interaction")


    def swap_lists(self, l1, l2):
        self.query_one(f"#{l1}", OptionList).disabled = True
        target = self.query_one(f"#{l2}", OptionList)
        target.disabled = False
        target.focus()
        self.query_one("#result_msg", Label).update("")  # Clear previous output
