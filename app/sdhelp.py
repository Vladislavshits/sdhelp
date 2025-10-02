import sys
import os
import logging
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton,
                           QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QLabel, QTabWidget)
from PyQt6.QtCore import Qt, QFile, QTextStream
from PyQt6.QtGui import QFont

# Добавляем путь к текущей директории в sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Настройка логирования
def setup_logging():
    log_dir = os.path.join(os.path.dirname(current_dir), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f'sdhelp_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

    return logging.getLogger(__name__)

logger = setup_logging()

# Импорты для экранов
from screens.games_screen import GamesScreen
from screens.programs_screen import ProgramsScreen
from screens.steamos_screen import SteamOSScreen
from screens.network_screen import NetworkScreen
from config import config


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        logger.info("Инициализация главного окна")
        self.initUI()
        self.loadStyles()

    def initUI(self):
        # Создание центрального виджета
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Установка окна на весь экран
        self.showFullScreen()
        self.setWindowTitle('SD Help - Настройка Steam Deck')

        logger.info("Главное окно настроено на полноэкранный режим")

        # Создание основного layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 100, 50, 50)

        # Добавление растягивающегося пространства сверху
        main_layout.addStretch(1)

        # Создание layout для кнопок
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(30)
        buttons_layout.setContentsMargins(100, 0, 100, 0)

        # Создание кнопок
        self.autoSetupBtn = QPushButton('Настроить за один клик')
        self.customSetupBtn = QPushButton('Выбрать исправления самостоятельно')

        # Настройка шрифтов для кнопок
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)

        self.autoSetupBtn.setFont(font)
        self.customSetupBtn.setFont(font)

        # Установка минимальных размеров кнопок
        self.autoSetupBtn.setMinimumHeight(80)
        self.customSetupBtn.setMinimumHeight(80)

        # Подключение сигналов
        self.autoSetupBtn.clicked.connect(self.autoSetup)
        self.customSetupBtn.clicked.connect(self.customSetup)

        # Добавление кнопок в layout
        buttons_layout.addWidget(self.autoSetupBtn)
        buttons_layout.addWidget(self.customSetupBtn)

        # Добавление кнопок в основной layout
        main_layout.addLayout(buttons_layout)

        # Добавление растягивающегося пространства посередине
        main_layout.addStretch(1)

        # Создание нижней панели
        bottom_layout = QVBoxLayout()

        # Кнопка выхода
        self.exitBtn = QPushButton('Выход')
        self.exitBtn.setMinimumHeight(50)
        self.exitBtn.setFont(font)
        self.exitBtn.clicked.connect(self.close)

        # Текст версии
        version_label = QLabel(f'Версия {config.get("version", "0.1")}')
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet("color: white; font-size: 14px; margin-top: 10px;")

        bottom_layout.addWidget(self.exitBtn)
        bottom_layout.addWidget(version_label)

        main_layout.addLayout(bottom_layout)

        central_widget.setLayout(main_layout)

    def loadStyles(self):
        """Загрузка стилей из файла"""
        try:
            style_path = os.path.join(current_dir, "styles.qss")
            style_file = QFile(style_path)
            if style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
                stream = QTextStream(style_file)
                self.setStyleSheet(stream.readAll())
                style_file.close()
                logger.info("Стили успешно загружены")
        except Exception as e:
            logger.error(f"Ошибка загрузки стилей: {e}")
            self.applyDefaultStyles()

    def applyDefaultStyles(self):
        """Стандартные стили если файл не найден"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #1e1e2e, stop: 1 #2d2b42);
            }
            QPushButton {
                background-color: #5d4e7b;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6d5d8a;
                border: 2px solid #ffffff;
            }
            QPushButton:pressed {
                background-color: #4a3e62;
            }
        """)

    def autoSetup(self):
        """Обработчик кнопки автоматической настройки"""
        logger.info("Нажата кнопка 'Настроить за один клик'")
        QMessageBox.information(self, "Автонастройка",
                               "Функция автоматической настройки будет реализована в будущем")

    def customSetup(self):
        """Обработчик кнопки выбора исправлений"""
        logger.info("Нажата кнопка 'Выбрать исправления самостоятельно'")
        self.custom_screen = CustomFixScreen()
        self.custom_screen.back_button.clicked.connect(self.showMainScreen)
        self.setCentralWidget(self.custom_screen)

    def showMainScreen(self):
        """Возврат на главный экран"""
        logger.info("Возврат на главный экран")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.initUI()

    def keyPressEvent(self, event):
        """Обработка нажатий клавиш"""
        if event.key() == Qt.Key.Key_Escape:
            logger.info("Нажата клавиша Escape - выход из программы")
            self.close()
        else:
            super().keyPressEvent(event)


class CustomFixScreen(QWidget):
    def __init__(self):
        super().__init__()
        logger.info("Инициализация экрана выбора исправлений")
        self.initUI()
        self.loadStyles()

    def initUI(self):
        # Основной layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Заголовок
        title_label = QLabel("Выбор исправлений")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white; margin: 20px;")

        main_layout.addWidget(title_label)

        # Создание вкладок
        self.tabs = QTabWidget()

        # Создание экранов для каждой вкладки
        self.games_screen = GamesScreen()
        self.programs_screen = ProgramsScreen()
        self.steamos_screen = SteamOSScreen()
        self.network_screen = NetworkScreen()

        # Добавление вкладок
        self.tabs.addTab(self.games_screen, "🎮 Игры")
        self.tabs.addTab(self.programs_screen, "📱 Программы")
        self.tabs.addTab(self.steamos_screen, "⚙️ SteamOS")
        self.tabs.addTab(self.network_screen, "🌐 Сеть")

        main_layout.addWidget(self.tabs)

        # Панель с кнопкой назад
        bottom_layout = QHBoxLayout()

        # Кнопка назад
        self.back_button = QPushButton("Назад")
        self.back_button.setMinimumHeight(50)
        back_font = QFont()
        back_font.setPointSize(14)
        back_font.setBold(True)
        self.back_button.setFont(back_font)

        bottom_layout.addWidget(self.back_button)
        bottom_layout.addStretch(1)

        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def loadStyles(self):
        """Загрузка стилей из файла"""
        try:
            style_path = os.path.join(os.path.dirname(__file__), "styles.qss")
            style_file = QFile(style_path)
            if style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
                stream = QTextStream(style_file)
                self.setStyleSheet(stream.readAll())
                style_file.close()
        except Exception as e:
            logger.error(f"Ошибка загрузки стилей: {e}")


def main():
    logger.info("Запуск приложения SD Help")
    app = QApplication(sys.argv)

    # Установка стиля приложения
    app.setStyle('Fusion')

    window = MainWindow()
    window.show()

    logger.info("Приложение успешно запущено")

    try:
        sys.exit(app.exec())
    except Exception as e:
        logger.error(f"Ошибка в главном цикле приложения: {e}")
        raise


if __name__ == '__main__':
    main()
