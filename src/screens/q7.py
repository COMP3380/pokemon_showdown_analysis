from textual import on
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button, OptionList, Label, DataTable, Static
from textual.containers import Horizontal, Container
from textual.widgets.option_list import Option
from textual.screen import Screen
from textual.binding import Binding
from .components.vim_option_list import VimOptionList


class Q7(Screen):
    TITLE = "Noob Pokemon Analysis"
    CSS_PATH = "styles/stats.tcss"

    BINDINGS = [
        ("Ctrl-q", "quit", "Quit"),
        ("m", "menu", "Menu"),
        ("b", "back", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Select Period to analyze 'Noob Pokemon' (Highest Usage Drop-off).", id="l1")

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

        with Container(id="input_container"):
            yield Button("Run Analysis", id="run_btn", variant="primary", disabled=True)

        yield Footer()

    def on_mount(self):
        self.query_one("#month", OptionList).focus()

    def action_menu(self):
        self.reset_form()
        self.app.switch_screen("menu")

    def action_back(self):
        self.reset_form()
        self.app.pop_screen()

    def reset_form(self):
        self.query_one("#run_btn", Button).disabled = True
        self.query_one("#month", OptionList).focus()

    @on(OptionList.OptionSelected)
    def choose_option(self, event: OptionList.OptionSelected) -> None:
        if event.option_list.id == "month":
            setattr(self.app, "period", "2025-" + event.option.id)
            self.query_one("#run_btn", Button).disabled = False
            self.query_one("#run_btn", Button).focus()

    @on(Button.Pressed, "#run_btn")
    def action_run_btn(self):
        self.run_analysis()

    def run_analysis(self):
        self.app.push_screen(Q7Results())


class Q7Results(Screen):
    TITLE = "Noob Pokemon Results"
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

        msg = self.query_one("#status_msg", Static)
        msg.update(
            f"Identifying 'Noob Pokemon' across all metagames in {period}...")

        sql = """
        WITH MetagameHighestCutoff AS
        (SELECT metagame, MAX(cutoff) as maxCutoff
        FROM PokemonUsage
        GROUP BY metagame),

        MetagameLowestCutoff AS
        (SELECT metagame, MIN(cutoff) as minCutoff
        FROM PokemonUsage
        GROUP BY metagame),

        PokemonUsageAtPeriod AS
        (SELECT metagame, cutoff, pokemon, usage
        FROM PokemonUsage
        WHERE period = %s),

        HighestCutoffUsage AS
        (SELECT PokemonUsageAtPeriod.metagame, maxCutoff, pokemon, usage
        FROM PokemonUsageAtPeriod
        INNER JOIN MetagameHighestCutoff ON PokemonUsageAtPeriod.metagame = MetagameHighestCutoff.metagame
        AND PokemonUsageAtPeriod.cutoff = MetagameHighestCutoff.maxCutoff),

        LowestCutoffUsage AS
        (SELECT PokemonUsageAtPeriod.metagame, minCutoff, pokemon, usage
        FROM PokemonUsageAtPeriod
        INNER JOIN MetagameLowestCutoff ON PokemonUsageAtPeriod.metagame = MetagameLowestCutoff.metagame
        AND PokemonUsageAtPeriod.cutoff = MetagameLowestCutoff.minCutoff),

        DiffUsage AS
        (SELECT HighestCutoffUsage.metagame, 
               HighestCutoffUsage.pokemon, 
               LowestCutoffUsage.usage - HighestCutoffUsage.usage AS usageDiff
        FROM HighestCutoffUsage
        INNER JOIN LowestCutoffUsage ON HighestCutoffUsage.metagame = LowestCutoffUsage.metagame
        AND HighestCutoffUsage.pokemon = LowestCutoffUsage.pokemon),

        MetagameHighestDiff AS
        (SELECT metagame, 
               MAX(usageDiff) AS highestDiff
        FROM DiffUsage
        GROUP BY metagame)

        SELECT 
            DiffUsage.metagame,
            DiffUsage.pokemon,
            MetagameHighestDiff.highestDiff AS usageDifference
        FROM 
            DiffUsage
        INNER JOIN 
            MetagameHighestDiff ON DiffUsage.metagame = MetagameHighestDiff.metagame
                                AND DiffUsage.usageDiff = MetagameHighestDiff.highestDiff
        ORDER BY
            DiffUsage.metagame;
        """

        try:
            params = (period,)
            headers, rows = self.app.execute_query(sql, params)

            table = self.query_one("#results_table", DataTable)
            table.clear(columns=True)
            table.add_columns("Metagame", "Pokemon", "Usage Diff")
            table.add_rows(rows)
            msg.update("Query Completed Successfully.")

        except Exception as e:
            msg.update(f"Error executing query: {str(e)}")
