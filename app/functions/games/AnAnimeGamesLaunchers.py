from functions.base_function import BaseFunction

class AnAnimeGamesLaunchers(BaseFunction):
    """Запуск скрипта по установке лаунчеров"""

    @property
    def name(self):
        return "Установка лаунчеров для аниме игр"

    @property
    def description(self):
        return "Установка лаунчеров от An Anime Team "

    def apply(self):
        """Запускает установку лаунчеров и добавляет репозиторий flatpak для них"""
        self.logger.info("Установка аниме лаунчера...")
        return self.run_script("AnAnimeGamesLaunchers.sh")
