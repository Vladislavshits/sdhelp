from core.base_screen import BaseScreen

class NetworkScreen(BaseScreen):
    def __init__(self):
        super().__init__(
            title="Настройки сети",
            description="Оптимизация сетевых подключений",
            category="network"
        )
