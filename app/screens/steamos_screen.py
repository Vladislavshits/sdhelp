from core.base_screen import BaseScreen

class SteamOSScreen(BaseScreen):
    def __init__(self):
        super().__init__(
            title="Настройки SteamOS",
            description="Оптимизация и настройка SteamOS",
            category="steamos"
        )
