from textual.widgets import OptionList
from textual.binding import Binding


class VimOptionList(OptionList):
    """
    Reusable OptionList with Vim-style navigation bindings.
    """
    BINDINGS = [
        Binding("j", "cursor_down", show=False),
        Binding("k", "cursor_up", show=False),
        Binding("l", "select", show=False),
        Binding("right", "select", show=False),
    ]
