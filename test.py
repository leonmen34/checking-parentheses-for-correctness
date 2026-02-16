from textual.app import App, ComposeResult
from textual.widgets import Input, Label, Button, Static
from textual.containers import Horizontal, Vertical

class BracketTable(Vertical):
    """Таблица для ввода пар скобок"""

    def __init__(self, rows: int = 5):
        super().__init__()
        self.rows = rows
        self.inputs = []  # храним все Input виджеты

    def compose(self) -> ComposeResult:
        yield Label("[bold]Ввод пар скобок[/bold]")
        for i in range(self.rows):
            with Horizontal():
                open_input = Input(placeholder="Открывающая скобка", id=f"open-{i}")
                close_input = Input(placeholder="Закрывающая скобка", id=f"close-{i}")
                self.inputs.append((open_input, close_input))
                yield open_input
                yield close_input
        yield Button("Сохранить", id="save-btn")

class SplitApp(App):
    def compose(self) -> ComposeResult:
        yield BracketTable(rows=5)
        yield Static("Результат будет тут", id="res-text")

    def on_button_pressed(self, event):
        if event.button.id == "save-btn":
            table = self.query_one(BracketTable)
            pairs = []
            for open_input, close_input in table.inputs:
                o = open_input.value.strip()
                c = close_input.value.strip()
                if o and c:
                    pairs.append([o, c])
            self.query_one("#res-text", Static).update(str(pairs))

if __name__ == "__main__":
    app = SplitApp()
    app.run()
