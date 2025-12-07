from textual import on
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button, OptionList, Label, Input, DataTable, Static
from textual.containers import Horizontal, Container
from textual.widgets.option_list import Option
from textual.screen import Screen
from textual.binding import Binding
from .components.vim_option_list import VimOptionList


class Q5(Screen):
    TITLE = "Best Pairs Analysis"
    CSS_PATH = "styles/stats.tcss"

    BINDINGS = [
        ("Ctrl-q", "quit", "Quit"),
        ("m", "menu", "Menu"),
        ("b", "back", "Back"),
        Binding("h,left", "prevlist", "Previous Option", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Select Metagame, Cutoff, and enter Top N count.", id="l1")

        with Horizontal():
            yield VimOptionList(
                Option("Overused (OU)", id="OU"),
                Option("Ubers", id="Ubers"),
                Option("UnderUsed (UU)", id="UU"),
                Option("RarelyUsed (RU)", id="RU"),
                Option("NeverUsed (NU)", id="NU"),
                Option("PU", id="PU"),
                Option("ZU", id="ZU"),
                id="metagame",
                disabled=False
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

        with Container(id="input_container"):
            yield Label("Analyze Top N Pairs:")
            yield Input(placeholder="e.g. 30", id="top_n_input", type="integer")
            yield Button("Run Analysis", id="run_btn", variant="primary", disabled=True)

        yield Footer()

    def action_menu(self):
        self.reset_form()
        self.app.switch_screen("menu")

    def action_back(self):
        self.reset_form()
        self.app.pop_screen()

    def reset_form(self):
        self.query_one("#cutoff", OptionList).disabled = True
        self.query_one("#metagame", OptionList).disabled = False
        self.query_one("#metagame", OptionList).focus()

        self.query_one("#top_n_input", Input).value = ""
        self.query_one("#run_btn", Button).disabled = True

    def action_prevlist(self):
        metagame = self.query_one("#metagame", OptionList)
        cutoff = self.query_one("#cutoff", OptionList)

        if not cutoff.disabled:
            metagame.disabled = False
            cutoff.disabled = True
            metagame.focus()

    @on(OptionList.OptionSelected)
    def choose_option(self, event: OptionList.OptionSelected) -> None:
        if event.option_list.id == "metagame":
            setattr(self.app, "metagame", event.option.id)
            self.swap_lists("metagame", "cutoff")

            # Logic for OU-specific cutoffs
            cutoff = self.query_one("#cutoff", OptionList)
            for option in cutoff.options:
                if event.option.id == "OU":
                    if option.id == "1760":
                        option.disabled = True
                    if option.id == "1825":
                        option.disabled = False
                else:
                    if option.id == "1760":
                        option.disabled = False
                    if option.id == "1825":
                        option.disabled = True

            self.check_submission_ready()

        elif event.option_list.id == "cutoff":
            setattr(self.app, "cutoff", event.option.id)
            self.query_one("#top_n_input", Input).focus()
            self.check_submission_ready()

    @on(Input.Changed, "#top_n_input")
    def on_input_change(self, event: Input.Changed):
        self.check_submission_ready()

    @on(Input.Submitted, "#top_n_input")
    def on_input_submit(self, event: Input.Submitted):
        if self.is_form_valid():
            self.run_analysis()

    def is_form_valid(self) -> bool:
        metagame = getattr(self.app, "metagame", "")
        cutoff = getattr(self.app, "cutoff", "")
        input_val = self.query_one("#top_n_input", Input).value

        return (metagame and cutoff and
                input_val.isdigit() and int(input_val) > 0)

    def check_submission_ready(self):
        btn = self.query_one("#run_btn", Button)
        if self.is_form_valid():
            btn.disabled = False
            setattr(self.app, "q5_top_n", int(
                self.query_one("#top_n_input", Input).value))
        else:
            btn.disabled = True

    @on(Button.Pressed, "#run_btn")
    def action_run_btn(self):
        self.run_analysis()

    def run_analysis(self):
        self.app.push_screen(Q5Results())

    def swap_lists(self, l1_str, l2_str):
        l1 = self.query_one(f"#{l1_str}", OptionList)
        l2 = self.query_one(f"#{l2_str}", OptionList)
        l2.disabled = False
        l1.disabled = True
        l2.focus()


class Q5Results(Screen):
    TITLE = "Best Pairs Results"
    CSS_PATH = "styles/stats.tcss"

    BINDINGS = [
        ("Ctrl-q", "quit", "Quit"),
        ("m", "menu", "Menu"),
        ("b", "back", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Loading...", id="status_msg")
        yield DataTable(id="results_table")
        yield Footer()

    def on_mount(self):
        self.run_query()

    def action_menu(self):
        self.app.switch_screen("menu")

    def action_back(self):
        self.app.pop_screen()

    def run_query(self):
        metagame = getattr(self.app, "metagame")
        cutoff = getattr(self.app, "cutoff")
        top_n = getattr(self.app, "q5_top_n")

        msg = self.query_one("#status_msg", Static)
        msg.update(
            f"Analyzing Top {top_n} Pairs in {metagame} (Cutoff: {cutoff})...")

        sql = """
        SELECT TOP (%s) p1.name, p2.name, t_out.usage
        FROM TeammateUsage t_out
        JOIN Pokemon p1 ON t_out.pokemonCurrent = p1.id
        JOIN Pokemon p2 ON t_out.pokemonTeammate = p2.id
        WHERE t_out.metagame = %s
          AND t_out.cutoff = %s
          AND t_out.pokemonCurrent < t_out.pokemonTeammate
          AND EXISTS (
              SELECT 1
              FROM TeammateUsage t_in
              WHERE t_in.metagame = t_out.metagame
                AND t_in.cutoff = t_out.cutoff
                AND t_in.pokemonCurrent = t_out.pokemonCurrent
                AND t_in.pokemonTeammate = t_out.pokemonTeammate
                AND t_in.period != t_out.period
          )
        ORDER BY t_out.usage DESC;
        """

        try:
            params = (top_n, metagame, cutoff)
            headers, rows = self.app.execute_query(sql, params)

            table = self.query_one("#results_table", DataTable)
            table.clear(columns=True)
            table.add_columns("Pokemon 1", "Pokemon 2", "Usage")
            table.add_rows(rows)
            msg.update("Query Completed Successfully.")

        except Exception as e:
            msg.update(f"Error executing query: {str(e)}")
