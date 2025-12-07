from textual import on
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button, OptionList, Label, DataTable, Static
from textual.containers import Horizontal, Container
from textual.widgets.option_list import Option
from textual.screen import Screen
from textual.binding import Binding
from .components.vim_option_list import VimOptionList


class Q8(Screen):
    TITLE = "Effectiveness/Counter Analysis"
    CSS_PATH = "styles/stats.tcss"

    BINDINGS = [
        ("Ctrl-q", "quit", "Quit"),
        ("m", "menu", "Menu"),
        ("b", "back", "Back"),
        Binding("h,left", "prevlist", "Previous Option", show=False),
    ]

    TYPES = [
        "Normal", "Fire", "Water", "Grass", "Electric", "Ice",
        "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug",
        "Rock", "Ghost", "Dragon", "Steel", "Dark", "Fairy"
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Select Counter Type (Type 1) and Target Type (Type 2).", id="l1")

        with Horizontal():
            yield VimOptionList(
                *[Option(t, id=t) for t in self.TYPES],
                id="type1",
                disabled=False
            )
            yield VimOptionList(
                *[Option(t, id=t) for t in self.TYPES],
                id="type2",
                disabled=True
            )

        with Container(id="input_container"):
            yield Button("Run Analysis", id="run_btn", variant="primary", disabled=True)

        yield Footer()

    def action_menu(self):
        self.reset_form()
        self.app.switch_screen("menu")

    def action_back(self):
        self.reset_form()
        self.app.pop_screen()

    def reset_form(self):
        self.query_one("#type2", OptionList).disabled = True
        self.query_one("#type1", OptionList).disabled = False
        self.query_one("#type1", OptionList).focus()
        self.query_one("#run_btn", Button).disabled = True

        if hasattr(self.app, "q8_type1"):
            delattr(self.app, "q8_type1")
        if hasattr(self.app, "q8_type2"):
            delattr(self.app, "q8_type2")

    def action_prevlist(self):
        t1 = self.query_one("#type1", OptionList)
        t2 = self.query_one("#type2", OptionList)

        if not t2.disabled:
            t1.disabled = False
            t2.disabled = True
            t1.focus()

    @on(OptionList.OptionSelected)
    def choose_option(self, event: OptionList.OptionSelected) -> None:
        if event.option_list.id == "type1":
            setattr(self.app, "q8_type1", event.option.id)
            self.swap_lists("type1", "type2")
            self.check_submission_ready()

        elif event.option_list.id == "type2":
            setattr(self.app, "q8_type2", event.option.id)
            self.check_submission_ready()
            # Move focus to button since this is the last list
            self.query_one("#run_btn", Button).focus()

    def check_submission_ready(self):
        t1 = getattr(self.app, "q8_type1", "")
        t2 = getattr(self.app, "q8_type2", "")

        btn = self.query_one("#run_btn", Button)
        if t1 and t2:
            btn.disabled = False
        else:
            btn.disabled = True

    @on(Button.Pressed, "#run_btn")
    def action_run_btn(self):
        self.run_analysis()

    def run_analysis(self):
        self.app.push_screen(Q8Results())

    def swap_lists(self, l1_str, l2_str):
        l1 = self.query_one(f"#{l1_str}", OptionList)
        l2 = self.query_one(f"#{l2_str}", OptionList)
        l2.disabled = False
        l1.disabled = True
        l2.focus()


class Q8Results(Screen):
    TITLE = "Counter Effectiveness Results"
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
        type1 = getattr(self.app, "q8_type1")
        type2 = getattr(self.app, "q8_type2")

        msg = self.query_one("#status_msg", Static)
        msg.update(
            f"Analyzing effectiveness of {type1} counters against top {type2} Pokemon...")

        sql = """
        WITH LatestPeriod AS (
            SELECT TOP 1 id
            FROM Period
            ORDER BY endDate DESC
        ),

        HighestCutoffMetagame AS (
            SELECT metagame, MAX(cutoff) as maxCutoff
            FROM PokemonUsage
            GROUP BY metagame
        ),

        RankedType2PokemonUsage AS (
            SELECT PokemonUsage.metagame, PokemonUsage.pokemon, PokemonUsage.usage,
            ROW_NUMBER() OVER (
                PARTITION BY PokemonUsage.metagame
                ORDER BY PokemonUsage.usage DESC
            ) as rn
            FROM PokemonUsage
            INNER JOIN Pokemon ON PokemonUsage.pokemon = Pokemon.id
            INNER JOIN LatestPeriod ON PokemonUsage.period = LatestPeriod.id
            INNER JOIN HighestCutoffMetagame ON PokemonUsage.metagame = HighestCutoffMetagame.metagame
            AND PokemonUsage.cutoff = HighestCutoffMetagame.maxCutoff
            WHERE (Pokemon.type1 = %s OR Pokemon.type2 = %s)
        ),

        Top5Type2Pokemon AS (
            SELECT metagame, pokemon
            FROM RankedType2PokemonUsage
            WHERE rn <= 5
        ),

        FilteredCounters AS (
            SELECT pokemonOpposing, occurrence, koRate, switchRate
            FROM CheckAndCounter
            INNER JOIN Top5Type2Pokemon ON CheckAndCounter.pokemonCurrent = Top5Type2Pokemon.pokemon
            AND CheckAndCounter.metagame = Top5Type2Pokemon.metagame
            INNER JOIN LatestPeriod ON CheckAndCounter.period = LatestPeriod.id
            INNER JOIN HighestCutoffMetagame ON CheckAndCounter.metagame = HighestCutoffMetagame.metagame
            AND CheckAndCounter.cutoff = HighestCutoffMetagame.maxCutoff
        )

        SELECT 
          'Type 1 (' + %s + ') Counters' AS analysis_type,
          SUM(occurrence) AS total_occurrence,
          AVG(koRate) AS avg_ko_rate,
          AVG(switchRate) AS avg_switch_rate
        FROM FilteredCounters
        INNER JOIN Pokemon ON FilteredCounters.pokemonOpposing = Pokemon.id
        WHERE (Pokemon.type1 = %s OR Pokemon.type2 = %s)

        UNION ALL

        SELECT 
          'All Counters Average' AS analysis_type,
          SUM(occurrence) AS total_occurrence,
          AVG(koRate) AS avg_ko_rate,
          AVG(switchRate) AS avg_switch_rate
        FROM FilteredCounters;
        """

        try:
            params = (type2, type2, type1, type1, type1)
            headers, rows = self.app.execute_query(sql, params)

            table = self.query_one("#results_table", DataTable)
            table.clear(columns=True)
            table.add_columns("Analysis Type", "Total Occurrences",
                              "Avg KO Rate (%)", "Avg Switch Rate (%)")
            table.add_rows(rows)
            msg.update("Query Completed Successfully.")

        except Exception as e:
            msg.update(f"Error executing query: {str(e)}")
