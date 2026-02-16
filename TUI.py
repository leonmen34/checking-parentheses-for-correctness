from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, Label
from textual.containers import Horizontal, Vertical

import controller 

# --- КЛАСС ЛЕВОЙ ПАНЕЛИ (ПРОГРАММА) ---
class ProgramPanel(Vertical):
    def compose(self) -> ComposeResult:
        yield Label("[bold]Проверка скобок[/bold]")
        yield Input(placeholder="Введите текст здесь...", id="input-text")
        yield Static("Результат будет тут", id="res-text")

    

    def on_input_submitted(self, event: Input.Submitted):
        # self — это уже ProgramPanel
        input_widget = self.query_one("#input-text", Input)  # находим Input по id
        user_text = input_widget.value                       # получаем текст

        resultMain = controller.main(user_text)

        # Обновляем результат прямо здесь
        self.update_result(resultMain)

    
    def update_result(self, text: str) -> None:
        self.query_one("#res-text", Static).update(text)


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

    BINDINGS = [
        ("r", "run_task", "Запуск программы")
    ]

    def action_run_task(self) -> None:
        panel = self.query_one(ProgramPanel)

        input_widget = panel.query_one("#input-text", Input)
        user_text = input_widget.value

        result = "Программа закончено"

        panel.update_result(result)

if __name__ == "__main__":
    app = SplitApp()
    app.run()