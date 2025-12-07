from textual import on
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button, OptionList, Label, Input, DataTable, Static
from textual.containers import Horizontal, Container
from textual.widgets.option_list import Option
from textual.screen import Screen
from textual.binding import Binding
from .components.vim_option_list import VimOptionList


class Q3(Screen):
    TITLE = "Stat Viability Analysis"
    CSS_PATH = "styles/stats.tcss"

    BINDINGS = [
        ("Ctrl-q", "quit", "Quit"),
        ("m", "menu", "Menu"),
        ("b", "back", "Back"),
        Binding("h,left", "prevlist", "Previous Option", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Select Period, Metagame, Stat, and enter Top N count.", id="l1")

        with Horizontal():
            yield VimOptionList(
                Option("January", id="01", disabled=True),
                Option("February", id="02", disabled=True),
                Option("March", id="03", disabled=True),
                Option("April", id="04", disabled=True),
                Option("May", id="05", disabled=True),
                Option("June", id="06", disabled=True),
                Option("July", id="07"),
                Option("August", id="08"),
                Option("September", id="09"),
                Option("October", id="10", disabled=True),
                Option("November", id="11", disabled=True),
                Option("December", id="12", disabled=True),
                id="month",
                disabled=False
            )
            yield VimOptionList(
                Option("Overused (OU)", id="OU"),
                Option("Ubers", id="Ubers"),
                Option("UnderUsed (UU)", id="UU"),
                Option("RarelyUsed (RU)", id="RU"),
                Option("NeverUsed (NU)", id="NU"),
                Option("PU", id="PU"),
                Option("ZU", id="ZU"),
                id="metagame",
                disabled=True
            )
            yield VimOptionList(
                Option("HP", id="hp"),
                Option("Attack", id="attack"),
                Option("Defense", id="defense"),
                Option("Sp. Attack", id="spattack"),
                Option("Sp. Defense", id="spdefense"),
                Option("Speed", id="speed"),
                id="stat_to_analyze",
                disabled=True
            )

        with Container(id="input_container"):
            yield Label("Analyze Top N Pokemon (by TopGXE):")
            yield Input(placeholder="e.g. 50", id="top_n_input", type="integer")
            yield Button("Run Analysis", id="run_btn", variant="primary", disabled=True)

        yield Footer()

    def action_menu(self):
        self.reset_form()
        self.app.switch_screen("menu")

    def action_back(self):
        self.reset_form()
        self.app.pop_screen()

    def reset_form(self):
        # Reset lists logic
        self.query_one("#stat_to_analyze", OptionList).disabled = True
        self.query_one("#metagame", OptionList).disabled = True
        self.query_one("#month", OptionList).disabled = False

        # Focus first
        self.query_one("#month", OptionList).focus()

        self.query_one("#top_n_input", Input).value = ""
        self.query_one("#run_btn", Button).disabled = True

        # Clear app context vars
        if hasattr(self.app, "q3_stat"):
            delattr(self.app, "q3_stat")

    def action_prevlist(self):
        month = self.query_one("#month", OptionList)
        metagame = self.query_one("#metagame", OptionList)
        stat = self.query_one("#stat_to_analyze", OptionList)

        if not metagame.disabled:
            month.disabled = False
            metagame.disabled = True
            month.focus()
        elif not stat.disabled:
            metagame.disabled = False
            stat.disabled = True
            metagame.focus()

    @on(OptionList.OptionSelected)
    def choose_option(self, event: OptionList.OptionSelected) -> None:
        if event.option_list.id == "month":
            setattr(self.app, "period", "2025-" + event.option.id)
            self.swap_lists("month", "metagame")
            self.check_submission_ready()

        elif event.option_list.id == "metagame":
            setattr(self.app, "metagame", event.option.id)
            self.swap_lists("metagame", "stat_to_analyze")
            self.check_submission_ready()

        elif event.option_list.id == "stat_to_analyze":
            setattr(self.app, "q3_stat", event.option.id)
            # Focus input after last list
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
        period = getattr(self.app, "period", "")
        metagame = getattr(self.app, "metagame", "")
        stat = getattr(self.app, "q3_stat", "")
        input_val = self.query_one("#top_n_input", Input).value

        return (period and metagame and stat and
                input_val.isdigit() and int(input_val) > 0)

    def check_submission_ready(self):
        btn = self.query_one("#run_btn", Button)
        if self.is_form_valid():
            btn.disabled = False
            setattr(self.app, "q3_top_n", int(
                self.query_one("#top_n_input", Input).value))
        else:
            btn.disabled = True

    @on(Button.Pressed, "#run_btn")
    def action_run_btn(self):
        self.run_analysis()

    def run_analysis(self):
        self.app.push_screen(Q3Results())

    def swap_lists(self, l1_str, l2_str):
        l1 = self.query_one(f"#{l1_str}", OptionList)
        l2 = self.query_one(f"#{l2_str}", OptionList)
        l2.disabled = False
        l1.disabled = True
        l2.focus()


class Q3Results(Screen):
    TITLE = "Stat Viability Results"
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
        period = getattr(self.app, "period")
        metagame = getattr(self.app, "metagame")
        stat = getattr(self.app, "q3_stat")
        top_n = getattr(self.app, "q3_top_n")

        msg = self.query_one("#status_msg", Static)
        msg.update(
            f"Analyzing {stat} for Top {top_n} via TopGXE in {metagame} ({period})...")

        sql = f"""
        WITH top_pokemon_by_gxe AS (
            SELECT TOP (%s) pokemon AS id
            FROM RawPokemonCount
            WHERE metagame = %s AND period = %s
            ORDER BY topGXE DESC
        ),
        top_stat_av AS (
            SELECT AVG({stat}) AS top_stat_av
            FROM top_pokemon_by_gxe T
            JOIN Pokemon P ON P.id = T.id
        ),
        stat_av AS (
            SELECT AVG({stat}) AS stat_av FROM Pokemon
        ),
        stat_stdev AS (
            SELECT STDEVP({stat}) AS stat_stdev FROM Pokemon
        )
        SELECT 
            '{stat}' AS Stat,
            top_stat_av.top_stat_av AS [Top Avg],
            stat_av.stat_av AS [Global Avg],
            stat_stdev.stat_stdev AS [Global StDev],
            (top_stat_av.top_stat_av - stat_av.stat_av) / NULLIF(stat_stdev.stat_stdev, 0) AS [Z-Score]
        FROM top_stat_av, stat_av, stat_stdev;
        """

        try:
            params = (top_n, metagame, period)
            headers, rows = self.app.execute_query(sql, params)

            table = self.query_one("#results_table", DataTable)
            table.clear(columns=True)
            table.add_columns(*headers)
            table.add_rows(rows)
            msg.update("Query Completed Successfully.")

        except Exception as e:
            msg.update(f"Error executing query: {str(e)}")
