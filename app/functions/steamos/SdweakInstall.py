from functions.base_function import BaseFunction

class SdweakInstall(BaseFunction):
    """Скачивает и запускает установщик SDWEAK https://github.com/Taskerer/SDWEAK"""

    @property
    def name(self):
        return "SDWEAK"

    @property
    def description(self):
        return "Набор оптимизаций для Steam Deck, улучшающий производительность и отзывчивость в целом."

    def apply(self):
        """Удаляет старый скрипт при его наличии, скачивает скрипт и запускает его в /tmp"""
        self.logger.info("Установка SDWEAK")
        return self.run_script("SDWEAK_Install.sh")
