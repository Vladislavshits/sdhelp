from functions.base_function import BaseFunction

class LocaleGen(BaseFunction):
    """Генерация локалей"""

    @property
    def name(self):
        return "Генерация локалей"

    @property
    def description(self):
        return "Генерирует локали для системы. В основном необходимо для запуска PortProton после смены языка рабочего стола"

    def apply(self):
        """Генерация локалей"""
        self.logger.info("Генерируем локали...")
        return self.run_script("locale_gen.sh")
