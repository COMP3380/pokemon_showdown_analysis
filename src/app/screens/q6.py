from textual import on
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button, Label, Input, DataTable, Static
from textual.containers import Container
from textual.screen import Screen


class Q6(Screen):
    TITLE = "Diverse Movesets Analysis"
    CSS_PATH = "styles/stats.tcss"

    BINDINGS = [
        ("Ctrl-q", "quit", "Quit"),
        ("m", "menu", "Menu"),
        ("b", "back", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Enter Top N count to see Pokemon with the widest movepools.", id="l1")

        with Container(id="input_container"):
            yield Label("Analyze Top N Pokemon:")
            yield Input(placeholder="e.g. 50", id="top_n_input", type="integer")
            yield Button("Run Analysis", id="run_btn", variant="primary", disabled=True)

        yield Footer()

    def on_mount(self):
        self.query_one("#top_n_input", Input).focus()

    def action_menu(self):
        self.reset_form()
        self.app.switch_screen("menu")

    def action_back(self):
        self.reset_form()
        self.app.pop_screen()

    def reset_form(self):
        self.query_one("#top_n_input", Input).value = ""
        self.query_one("#run_btn", Button).disabled = True

    @on(Input.Changed, "#top_n_input")
    def on_input_change(self, event: Input.Changed):
        self.check_submission_ready()

    @on(Input.Submitted, "#top_n_input")
    def on_input_submit(self, event: Input.Submitted):
        if self.is_form_valid():
            self.run_analysis()

    def is_form_valid(self) -> bool:
        input_val = self.query_one("#top_n_input", Input).value
        return input_val.isdigit() and int(input_val) > 0

    def check_submission_ready(self):
        btn = self.query_one("#run_btn", Button)
        if self.is_form_valid():
            btn.disabled = False
            setattr(self.app, "q6_top_n", int(
                self.query_one("#top_n_input", Input).value))
        else:
            btn.disabled = True

    @on(Button.Pressed, "#run_btn")
    def action_run_btn(self):
        self.run_analysis()

    def run_analysis(self):
        self.app.push_screen(Q6Results())


class Q6Results(Screen):
    TITLE = "Diverse Movesets Results"
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
        top_n = getattr(self.app, "q6_top_n")

        msg = self.query_one("#status_msg", Static)
        msg.update(f"Analyzing Top {top_n} Pokemon by Movepool Size...")

        sql = """
        SELECT TOP (%s) p.name, count(DISTINCT plm.move) AS num_moves
        FROM Pokemon p
        JOIN PokemonLearnsMove plm ON plm.pokemon = p.id
        GROUP BY p.id, p.name
        ORDER BY num_moves DESC;
        """

        try:
            params = (top_n,)
            headers, rows = self.app.execute_query(sql, params)

            table = self.query_one("#results_table", DataTable)
            table.clear(columns=True)
            table.add_columns("Pokemon", "Learnable Moves")
            table.add_rows(rows)
            msg.update("Query Completed Successfully.")

        except Exception as e:
            msg.update(f"Error executing query: {str(e)}")
