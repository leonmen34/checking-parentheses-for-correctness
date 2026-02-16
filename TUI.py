from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, Label
from textual.containers import Horizontal, Vertical

# --- КЛАСС ЛЕВОЙ ПАНЕЛИ (ПРОГРАММА) ---
class ProgramPanel(Vertical):
    def compose(self) -> ComposeResult:
        yield Label("[bold]Проверка скобок[/bold]")
        yield Input(placeholder="Введите текст здесь...")
        yield Static("Результат будет тут", id="res-text")

# --- КЛАСС ПРАВОЙ ПАНЕЛИ (НАСТРОЙКИ) ---
class SettingsPanel(Vertical):
    def compose(self) -> ComposeResult:
        yield Label("[bold]Настройки[/bold]")
        yield Static("• JSON файл: загружен")
        yield Static("• Тема: Темная")
        yield Static("• Версия: 1.0.0")

class SplitApp(App):
    TITLE = "BracketChecker Pro"

    CSS = """
    /* Стили для ProgramPanel (используем имя класса или ID) */
    ProgramPanel {
        width: 60%;
        height: 100%;
        border-right: solid white;
        background: $primary-darken-2;
        padding: 1;
    }

    /* Стили для SettingsPanel */
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
            # Просто вызываем наши классы как обычные виджеты
            yield ProgramPanel() 
            yield SettingsPanel()
        yield Footer()

if __name__ == "__main__":
    app = SplitApp()
    app.run()