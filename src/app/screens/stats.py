from textual import on
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button, OptionList, Label
from textual.containers import Horizontal
from textual.widgets.option_list import Option
from textual.screen import Screen
from textual.binding import Binding

class Stats(Screen):
    TITLE = "Stats"
    CSS_PATH = "styles/stats.tcss"

    BINDINGS = [
        ("Ctrl-q", "quit", "Quit"),
        ("m", "menu", "Menu"),
        ("b", "back", "Back"),
        Binding("h,left", "prevlist", "Previous OptionList", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Please select a Period, Metagame, and Cutoff!", id="l1")
        with Horizontal():
            yield VimOptionList(
                Option("January", id="jan", disabled=True),
                Option("February", id="feb", disabled=True),
                Option("March", id="mar", disabled=True),
                Option("April", id="apr", disabled=True),
                Option("May", id="may", disabled=True),
                Option("June", id="jun", disabled=True),
                Option("July", id="jul"),
                Option("August", id="aug"),
                Option("September", id="sep"),
                Option("October", id="oct"),
                Option("November", id="nov", disabled=True),
                Option("December", id="dec", disabled=True),
                id="month",
                disabled=False
            )
            yield VimOptionList(
                Option("Overused (OU)", id="ou"),
                Option("Ubers", id="ubers"),
                Option("UnderUsed (UU)", id="uu"),
                Option("RarelyUsed (RU)", id="ru"),
                Option("NeverUsed (NU)", id="nu"),
                Option("PU", id="pu"),
                Option("ZU", id="zu"),
                id="metagame",
                disabled=True
            )
            yield VimOptionList(
                Option("0", id="0"),
                Option("1500", id="1500", disabled=True),
                Option("1630", id="1630", disabled=True),
                Option("1695", id="1695", disabled=True),
                Option("1760", id="1760"),
                Option("1825", id="1825"),
                id="cutoff",
                disabled=True
            )
        yield Footer()

    def action_menu(self):
        # Make sure to reset lists
        self.swap_lists("cutoff", "month")
        self.swap_lists("metagame", "month")
        self.app.switch_screen("menu")

    def action_back(self):
        # Make sure to reset lists
        self.swap_lists("cutoff", "month")
        self.swap_lists("metagame", "month")
        self.app.pop_screen()

    # Go back to the previous OptionList
    def action_prevlist(self):
        # Get all lists
        month = self.query_one("#month", OptionList)
        metagame = self.query_one("#metagame", OptionList)
        cutoff = self.query_one("#cutoff", OptionList)

        if not metagame.disabled:
            month.disabled = False
            metagame.disabled = True
        elif not cutoff.disabled:
            metagame.disabled = False
            cutoff.disabled = True

    @on(OptionList.OptionSelected)
    def choose_month(self, event: OptionList.OptionSelected) -> None:
        if event.option_list.id == "month":
            self.log(f"Selected {event.option.prompt}")
            setattr(self.app, "period", event.option.id)
            self.swap_lists("month", "metagame")


        if event.option_list.id == "metagame":
            self.log(f"Selected {event.option.prompt}")
            setattr(self.app, "metagame", event.option.id)
            self.swap_lists("metagame", "cutoff")

            cutoff = self.query_one("#cutoff", OptionList)

            # OU has different cutoffs
            for option in cutoff.options:
                if event.option.id == "ou":
                    if option.id == "1760":
                        option.disabled = True
                    if option.id == "1825":
                        option.disabled = False
                else:
                    if option.id == "1760":
                        option.disabled = False
                    if option.id == "1825":
                        option.disabled = True

        if event.option_list.id == "cutoff":
            self.log(f"Selected {event.option.prompt}")
            setattr(self.app, "cutoff", event.option.id)
            self.app.push_screen("stats_p2")

    # Disable l1, Enable l2
    def swap_lists(self, l1_str, l2_str):
        l1 = self.query_one(f"#{l1_str}", OptionList)
        l2 = self.query_one(f"#{l2_str}", OptionList)
        l2.disabled = False
        l1.disabled = True

class VimOptionList(OptionList):
    BINDINGS = [
        Binding("j", "cursor_down", show=False),
        Binding("k", "cursor_up", show=False),
        Binding("l", "select", show=False),
        Binding("right", "select", show=False),
    ]
