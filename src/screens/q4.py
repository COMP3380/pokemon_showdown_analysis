from textual import on
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button, OptionList, Label, Input, DataTable, Static
from textual.containers import Horizontal, Container
from textual.widgets.option_list import Option
from textual.screen import Screen
from textual.binding import Binding
from .components.vim_option_list import VimOptionList


class Q4(Screen):
    TITLE = "Underrated Abilities Analysis"
    CSS_PATH = "styles/stats.tcss"

    BINDINGS = [
        ("Ctrl-q", "quit", "Quit"),
        ("m", "menu", "Menu"),
        ("b", "back", "Back"),
        Binding("h,left", "prevlist", "Previous Option", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Select Period, Metagame, and enter Top N count.", id="l1")

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

        with Container(id="input_container"):
            yield Label("Analyze Top N Abilities:")
            yield Input(placeholder="e.g. 10", id="top_n_input", type="integer")
            yield Button("Run Analysis", id="run_btn", variant="primary", disabled=True)

        yield Footer()

    def action_menu(self):
        self.reset_form()
        self.app.switch_screen("menu")

    def action_back(self):
        self.reset_form()
        self.app.pop_screen()

    def reset_form(self):
        self.query_one("#metagame", OptionList).disabled = True
        self.query_one("#month", OptionList).disabled = False
        self.query_one("#month", OptionList).focus()

        self.query_one("#top_n_input", Input).value = ""
        self.query_one("#run_btn", Button).disabled = True

    def action_prevlist(self):
        month = self.query_one("#month", OptionList)
        metagame = self.query_one("#metagame", OptionList)

        if not metagame.disabled:
            month.disabled = False
            metagame.disabled = True
            month.focus()

    @on(OptionList.OptionSelected)
    def choose_option(self, event: OptionList.OptionSelected) -> None:
        if event.option_list.id == "month":
            setattr(self.app, "period", "2025-" + event.option.id)
            self.swap_lists("month", "metagame")
            self.check_submission_ready()

        elif event.option_list.id == "metagame":
            setattr(self.app, "metagame", event.option.id)
            # Metagame is the last list, so focus input
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
        input_val = self.query_one("#top_n_input", Input).value

        return (period and metagame and
                input_val.isdigit() and int(input_val) > 0)

    def check_submission_ready(self):
        btn = self.query_one("#run_btn", Button)
        if self.is_form_valid():
            btn.disabled = False
            setattr(self.app, "q4_top_n", int(
                self.query_one("#top_n_input", Input).value))
        else:
            btn.disabled = True

    @on(Button.Pressed, "#run_btn")
    def action_run_btn(self):
        self.run_analysis()

    def run_analysis(self):
        self.app.push_screen(Q4Results())

    def swap_lists(self, l1_str, l2_str):
        l1 = self.query_one(f"#{l1_str}", OptionList)
        l2 = self.query_one(f"#{l2_str}", OptionList)
        l2.disabled = False
        l1.disabled = True
        l2.focus()


class Q4Results(Screen):
    TITLE = "Underrated Abilities Results"
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
        top_n = getattr(self.app, "q4_top_n")

        # Logic to determine cutoffs
        low_cutoff = 0
        high_cutoff = 1825 if metagame == "OU" else 1760

        msg = self.query_one("#status_msg", Static)
        msg.update(
            f"Analyzing Underrated Abilities (High: {high_cutoff}, Low: {low_cutoff}) in {metagame}...")

        sql = """
        SELECT TOP (%s) a.id, a.name, AVG(ab_out.usage) AS average_usage
        FROM Ability a
        JOIN AbilityUsage ab_out ON ab_out.ability = a.id
        WHERE ab_out.metagame = %s AND ab_out.period = %s
        AND ab_out.cutoff = %s
        AND a.id IN (
            SELECT ability FROM (
                SELECT TOP (%s) ab_in.ability AS ability, AVG(ab_in.usage) as av_top_usage
                FROM AbilityUsage ab_in
                WHERE ab_in.metagame = ab_out.metagame AND ab_in.period = ab_out.period
                AND ab_in.cutoff = %s
                GROUP BY ab_in.ability
                ORDER BY av_top_usage DESC
            ) as t
        )
        GROUP BY a.id, a.name
        ORDER BY average_usage;
        """

        try:
            params = (top_n, metagame, period, low_cutoff, top_n, high_cutoff)
            headers, rows = self.app.execute_query(sql, params)

            table = self.query_one("#results_table", DataTable)
            table.clear(columns=True)
            table.add_columns("ID", "Name", "Average Low Ladder Usage")
            table.add_rows(rows)
            msg.update("Query Completed Successfully.")

        except Exception as e:
            msg.update(f"Error executing query: {str(e)}")
