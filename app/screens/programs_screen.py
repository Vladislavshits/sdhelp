from core.base_screen import BaseScreen

class ProgramsScreen(BaseScreen):
    def __init__(self):
        super().__init__(
            title="Установка программ",
            description="Установите полезные программы для Steam Deck",
            category="programs"
        )
