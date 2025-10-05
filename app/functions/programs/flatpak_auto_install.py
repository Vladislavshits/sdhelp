from functions.base_function import BaseFunction

class FlatpakProgrammsInstall(BaseFunction): 
    """Установка базовых программ из Flatpak"""

    @property
    def name(self):
        return "Установка программ"

    @property
    def description(self):
        return "Скрипт для установки популярных программ для Steam Deck"

    def apply(self):
        """Установка программ из Flatpak"""
        self.logger.info("Установка программ из Flatpak...")
        return self.run_script("flatpak_autoinstall.sh")
