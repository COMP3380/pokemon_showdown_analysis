from textual import on
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button, OptionList, Label, Input, DataTable, Static
from textual.containers import Horizontal, Container
from textual.widgets.option_list import Option
from textual.screen import Screen
from textual.binding import Binding
from .components.vim_option_list import VimOptionList


class Q1(Screen):
    TITLE = "Base Stats Priority Analysis"
    CSS_PATH = "styles/stats.tcss"

    BINDINGS = [
        ("Ctrl-q", "quit", "Quit"),
        ("m", "menu", "Menu"),
        ("b", "back", "Back"),
        Binding("h,left", "prevlist", "Previous Option", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Select Period, Metagame, Cutoff, and enter Top N count.", id="l1")

        # Reuse the layout style from Stats
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
            yield Label("Analyze Top N Pokemon:")
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
        # Reset lists and input
        self.swap_lists("cutoff", "month")
        self.swap_lists("metagame", "month")
        self.query_one("#top_n_input", Input).value = ""
        self.query_one("#run_btn", Button).disabled = True

    def action_prevlist(self):
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
    def choose_option(self, event: OptionList.OptionSelected) -> None:
        if event.option_list.id == "month":
            setattr(self.app, "period", "2025-" + event.option.id)
            self.swap_lists("month", "metagame")
            self.check_submission_ready()

        elif event.option_list.id == "metagame":
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
            # Focus the input field after selecting the last option
            self.query_one("#top_n_input", Input).focus()
            self.check_submission_ready()

    @on(Input.Changed, "#top_n_input")
    def on_input_change(self, event: Input.Changed):
        self.check_submission_ready()

    @on(Input.Submitted, "#top_n_input")
    def on_input_submit(self, event: Input.Submitted):
        """Handle Enter key press in the input field"""
        if self.is_form_valid():
            self.run_analysis()

    def is_form_valid(self) -> bool:
        """Check if all required fields are populated and valid"""
        cutoff_val = getattr(self.app, "cutoff", "")
        metagame_val = getattr(self.app, "metagame", "")
        period_val = getattr(self.app, "period", "")

        input_val = self.query_one("#top_n_input", Input).value

        return (cutoff_val and metagame_val and period_val and
                input_val.isdigit() and int(input_val) > 0)

    def check_submission_ready(self):
        """Enable or disable the run button based on form validity"""
        btn = self.query_one("#run_btn", Button)
        if self.is_form_valid():
            btn.disabled = False
            # Store the top n value in app context
            setattr(self.app, "q1_top_n", int(
                self.query_one("#top_n_input", Input).value))
        else:
            btn.disabled = True

    @on(Button.Pressed, "#run_btn")
    def action_run_btn(self):
        self.run_analysis()

    def run_analysis(self):
        self.app.push_screen("q1_results")

    def swap_lists(self, l1_str, l2_str):
        l1 = self.query_one(f"#{l1_str}", OptionList)
        l2 = self.query_one(f"#{l2_str}", OptionList)
        l2.disabled = False
        l1.disabled = True


class Q1Results(Screen):
    TITLE = "Base Stats Priority Results"
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
        cutoff = getattr(self.app, "cutoff")
        top_n = getattr(self.app, "q1_top_n")

        msg = self.query_one("#status_msg", Static)
        msg.update(
            f"Analyzing Top {top_n} Pokemon in {metagame} ({period}, {cutoff})...")

        sql = """
        WITH stat_averages AS (
          SELECT 
            AVG(hp) AS hp_av,
            AVG(attack) AS attack_av,
            AVG(defense) AS defense_av,
            AVG(spattack) AS spattack_av,
            AVG(spdefense) AS spdefense_av,
            AVG(speed) AS speed_av
          FROM Pokemon
        ),
        stat_stdevs AS (
          SELECT 
            STDEVP(hp) AS hp_dev,
            STDEVP(attack) AS attack_dev,
            STDEVP(defense) AS defense_dev,
            STDEVP(spattack) AS spattack_dev,
            STDEVP(spdefense) AS spdefense_dev,
            STDEVP(speed) AS speed_dev
          FROM Pokemon
        ),
        top_used_pokemon AS (
          SELECT TOP (%s) pokemon AS id
          FROM PokemonUsage
          WHERE metagame = %s AND period = %s AND cutoff = %s
          ORDER BY usage DESC
        ),
        top_pokemon_stat_avs AS (
          SELECT 
            AVG(hp) AS hp_av_p,
            AVG(attack) AS attack_av_p,
            AVG(defense) AS defense_av_p,
            AVG(spattack) AS spattack_av_p,
            AVG(spdefense) AS spdefense_av_p,
            AVG(speed) AS speed_av_p
          FROM top_used_pokemon
          JOIN Pokemon ON Pokemon.id = top_used_pokemon.id
        ),
        z_scores AS (
          SELECT 
            (hp_av_p - hp_av) / hp_dev AS hp_z,
            (attack_av_p - attack_av) / attack_dev AS attack_z,
            (defense_av_p - defense_av) / defense_dev AS defense_z,
            (spattack_av_p - spattack_av) / spattack_dev AS spattack_z,
            (spdefense_av_p - spdefense_av) / spdefense_dev AS spdefense_z,
            (speed_av_p - speed_av) / speed_dev AS speed_z
          FROM top_pokemon_stat_avs, stat_averages, stat_stdevs
        )
        SELECT 'HP' AS stat, hp_z AS z_val FROM z_scores
        UNION ALL SELECT 'Attack', attack_z FROM z_scores
        UNION ALL SELECT 'Defense', defense_z FROM z_scores
        UNION ALL SELECT 'SpAttack', spattack_z FROM z_scores
        UNION ALL SELECT 'SpDefense', spdefense_z FROM z_scores
        UNION ALL SELECT 'Speed', speed_z FROM z_scores
        ORDER BY z_val DESC;
        """

        try:
            params = (top_n, metagame, period, cutoff)
            headers, rows = self.app.execute_query(sql, params)

            table = self.query_one("#results_table", DataTable)
            table.clear(columns=True)
            table.add_columns(*headers)
            table.add_rows(rows)
            msg.update("Query Completed Successfully.")

        except Exception as e:
            msg.update(f"Error executing query: {str(e)}")
