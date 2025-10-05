from core.base_screen import BaseScreen

class GamesScreen(BaseScreen):
    def __init__(self):
        super().__init__(
            title="Исправления для игр",
            description="Выберите исправление для конкретной игры", 
            category="games"
        )
