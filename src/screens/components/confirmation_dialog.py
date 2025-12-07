from textual.app import ComposeResult
from textual.widgets import Static, Button
from textual.message import Message
from textual import events

class ConfirmationDialog(Static):
    """A modal confirmation popup with Yes/No buttons."""

    DEFAULT_CSS = """
    ConfirmationDialog {
        layer: overlay;
        width: 40;
        height: 13;
        background: $panel;
        border: heavy $primary;
        padding: 1 2;
        content-align: center middle;
    }

    ConfirmationDialog .buttons {
        layout: horizontal;
        align-horizontal: center;
        margin-top: 1;
    }

    ConfirmationDialog Button {
        width: 10;
        margin: 0 1;
    }
    """

    class Yes(Message):
        """Sent when user confirms."""
        pass

    class No(Message):
        """Sent when user rejects."""
        pass

    def compose(self) -> ComposeResult:
        yield Static("Are you sure you want to delete and refresh the entire database? It will take about 5 minutes. You will know when it is done when this dialog box has disappeared.", id="prompt")

        with Static(classes="buttons"):
            yield Button("Yes", id="yes", variant="success")
            yield Button("No", id="no", variant="error")

    def on_mount(self):
        self.focus()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "yes":
            self.post_message(self.Yes())
            self.remove()
        elif event.button.id == "no":
            self.post_message(self.No())
            self.remove()
