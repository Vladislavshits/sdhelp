import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton,
                           QVBoxLayout, QWidget, QMessageBox)
from PyQt6.QtCore import Qt, QFile, QTextStream
from PyQt6.QtGui import QFont


class SDHelpWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadStyles()

    def initUI(self):
        # Создание центрального виджета
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Установка окна на весь экран
        self.showFullScreen()
        self.setWindowTitle('SD Help - Настройка Steam Deck')

        # Создание layout
        layout = QVBoxLayout()
        layout.setSpacing(30)
        layout.setContentsMargins(50, 100, 50, 100)

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
        layout.addWidget(self.autoSetupBtn)
        layout.addWidget(self.customSetupBtn)
        layout.addStretch(1)

        central_widget.setLayout(layout)

    def loadStyles(self):
        """Загрузка стилей из файла"""
        try:
            style_file = QFile("app/styles.qss")
            if style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
                stream = QTextStream(style_file)
                self.setStyleSheet(stream.readAll())
                style_file.close()
        except Exception as e:
            print(f"Ошибка загрузки стилей: {e}")
            # Стандартные стили если файл не найден
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #2b2b2b;
                }
                QPushButton {
                    background-color: #0078d4;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 15px;
                }
                QPushButton:hover {
                    background-color: #106ebe;
                }
                QPushButton:pressed {
                    background-color: #005a9e;
                }
            """)

    def autoSetup(self):
        """Обработчик кнопки автоматической настройки"""
        QMessageBox.information(self, "Автонастройка",
                               "Функция автоматической настройки будет реализована в будущем")

    def customSetup(self):
        """Обработчик кнопки выбора исправлений"""
        QMessageBox.information(self, "Выбор исправлений",
                               "Функция выбора исправлений будет реализована в будущем")

    def keyPressEvent(self, event):
        """Обработка нажатий клавиш"""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)


def main():
    app = QApplication(sys.argv)

    # Установка стиля приложения
    app.setStyle('Fusion')

    window = SDHelpWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
