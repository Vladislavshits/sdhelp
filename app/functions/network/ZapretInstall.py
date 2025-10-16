from functions.base_function import BaseFunction

class ZapretInstall(BaseFunction):
    """Запускает скрипт установки Zapret DPI Manager"""

    @property
    def name(self):
        return "Zapret DPI Manager"

    @property
    def description(self):
        return "Устанавливает Zapret DPI с интерфейсом настройки"

    def apply(self):
        """Скачивает архив, распаковывает файлы в ~/zapret и создаёт ярлык для запуска"""
        self.logger.info("Установка Zapret DPI Manager...")
        return self.run_script("Zapret_Install.sh")
