from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, Label
from textual.containers import Horizontal, Vertical
from textual.widgets import DataTable
import json
import controller  # твой модуль с main() и load_json()

# --- ЛЕВАЯ ПАНЕЛЬ ---
class ProgramPanel(Vertical):
    def compose(self) -> ComposeResult:
        yield Label("[bold]Проверка скобок[/bold]")
        yield Input(placeholder="Введите текст здесь...", id="input-text")
        yield Static("Результат будет тут", id="res-text")

    def on_input_submitted(self, event: Input.Submitted):
        input_widget = self.query_one("#input-text", Input)
        user_text = input_widget.value                      
        resultMain = controller.main(user_text)
        self.update_result(resultMain)

    def update_result(self, text: str) -> None:
        self.query_one("#res-text", Static).update(text)


# --- ПРАВАЯ ПАНЕЛЬ (Настройки) ---
class SettingsPanel(Vertical):
    CSS = """
    Horizontal {
        height: auto;
        width: 100%;
        padding: 1;
        gap: 1;
    }
    Input {
        expand: 1;
    }
    DataTable {
        height: 10;
        width: 100%;
    }
    """

    BINDINGS = [
        ("a", "add_bracket", "Добавить скобку"),
        ("d", "delete_bracket", "Удалить выбранную"),
        ("s", "save_brackets", "Сохранить в JSON"),
    ]

    def compose(self) -> ComposeResult:
        yield Label("[bold]Настройки[/bold]")
        # Горизонтальный контейнер для двух input
        
        self.open_input = Input(placeholder="Open", id="open-input")
        self.close_input = Input(placeholder="Close", id="close-input")
        yield self.open_input
        yield self.close_input
        # Таблица
        self.table = DataTable()
        yield self.table

    def on_mount(self) -> None:
        self.load_config()
        self.table.add_columns("ID", "Open", "Close")
        self.refresh_table()
        self.table.cursor_type = "row"

    # --- Работа с конфигом ---
    def load_config(self):
        APP_CONFIG = controller.load_json('settings.json') or {}
        self.brackets = APP_CONFIG.get("supported_brackets", [])

    def refresh_table(self):
        self.table.clear()
        for idx, (open_br, close_br) in enumerate(self.brackets, start=1):
            self.table.add_row(str(idx), open_br, close_br)

    # --- Actions биндов ---
    def action_add_bracket(self):
        open_br = self.query_one("#open-input", Input).value.strip()
        close_br = self.query_one("#close-input", Input).value.strip()
        if open_br and close_br and [open_br, close_br] not in self.brackets:
            self.brackets.append([open_br, close_br])
            self.refresh_table()
            # Очистка input
            self.query_one("#open-input", Input).value = ""
            self.query_one("#close-input", Input).value = ""

    def action_delete_bracket(self):
        if self.table.cursor_row is not None:
            del self.brackets[self.table.cursor_row]
            self.refresh_table()

    def action_save_brackets(self):
        APP_CONFIG = controller.load_json('settings.json') or {}
        APP_CONFIG["supported_brackets"] = self.brackets
        with open('settings.json', 'w', encoding='utf-8') as f:
            json.dump(APP_CONFIG, f, ensure_ascii=False, indent=4)
        self.app.notify("Скобки сохранены!")


# --- Основное приложение ---
class SplitApp(App):
    TITLE = "BracketChecker Pro"

    CSS = """
    ProgramPanel {
        width: 60%;
        height: 100%;
        border-right: solid white;
        background: $primary-darken-2;
        padding: 1;
    }

    SettingsPanel {
        width: 40%;
        height: 100%;
        background: $surface;
        padding: 1;
    }

    Label {
        margin: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield ProgramPanel()
            yield SettingsPanel()
        yield Footer()

    BINDINGS = [
        ("r", "run_task", "Запуск программы")
    ]

    def action_run_task(self) -> None:
        panel = self.query_one(ProgramPanel)
        input_widget = panel.query_one("#input-text", Input)
        user_text = input_widget.value
        result = controller.main(user_text)
        panel.update_result(result)


if __name__ == "__main__":
    SplitApp().run()