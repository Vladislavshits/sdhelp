from functions.base_function import BaseFunction

class OpenhFlatpakInstall(BaseFunction):
    """Запускает скрипт скачивания подходящего скрипта"""

    @property
    def name(self):
        return "Установка кодеков Openh264 из Github"

    @property
    def description(self):
        return "Скрипт для скачивания исходников, их компиляции и установки. Исправляет ошибку установки программ в Discover. Процесс занимает примерно 15 минут."

    def apply(self):
        """Проверяет наличие команды steamos-readonly и скачивает нужный скрипт в /tmp, откуда он и запускается."""
        self.logger.info("Компиляция библиотек Openh264...")
        return self.run_script("OpenhFlatpakInstall.sh")
