from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QScrollArea, QFrame, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import os
import sys

# Добавляем путь для импортов
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, current_dir)

from config import config


class ProgramsScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Основной layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Заголовок
        title_label = QLabel("Установка программ")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white; margin: 10px;")

        main_layout.addWidget(title_label)

        # Описание
        desc_label = QLabel("Установите полезные программы для Steam Deck:")
        desc_label.setStyleSheet("color: #cccccc; font-size: 14px; margin: 10px;")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(desc_label)

        # Создание scroll area
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.setSpacing(15)

        # Программы для установки
        programs = [
            {
                "name": "Zapret",
                "key": "zapret",
                "description": "Утилита для обхода блокировок и ограничений"
            },
            {
                "name": "Decky Loader",
                "key": "decky_loader",
                "description": "Загрузчик плагинов для кастомных настроек Steam Deck"
            }
        ]

        for program in programs:
            program_widget = self.createProgramWidget(program)
            scroll_layout.addWidget(program_widget)

        scroll_layout.addStretch(1)
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
            }
        """)

        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def createProgramWidget(self, program_data):
        """Создание виджета для программы"""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: rgba(93, 78, 123, 0.3);
                border-radius: 10px;
                padding: 15px;
            }
            QFrame:hover {
                background-color: rgba(109, 93, 138, 0.4);
            }
        """)

        layout = QHBoxLayout()

        # Текстовая информация
        text_layout = QVBoxLayout()

        name_label = QLabel(program_data["name"])
        name_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")

        desc_label = QLabel(program_data["description"])
        desc_label.setStyleSheet("color: #cccccc; font-size: 12px;")
        desc_label.setWordWrap(True)

        text_layout.addWidget(name_label)
        text_layout.addWidget(desc_label)
        text_layout.addStretch(1)

        # Кнопка установки/удаления
        install_button = QPushButton()
        install_button.setMinimumWidth(120)
        install_button.setMinimumHeight(40)

        # Проверяем статус установки
        is_installed = config.is_program_installed(program_data["key"])
        self.updateInstallButton(install_button, is_installed)

        # Подключаем обработчик
        install_button.clicked.connect(lambda checked, p=program_data: self.toggleProgramInstall(p))

        layout.addLayout(text_layout)
        layout.addWidget(install_button)

        widget.setLayout(layout)
        return widget

    def updateInstallButton(self, button, is_installed):
        """Обновление текста и стиля кнопки установки"""
        if is_installed:
            button.setText("Удалить")
            button.setStyleSheet("""
                QPushButton {
                    background-color: #d83b01;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #b32d00;
                }
            """)
        else:
            button.setText("Установить")
            button.setStyleSheet("""
                QPushButton {
                    background-color: #107c10;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #0d6b0d;
                }
            """)

    def toggleProgramInstall(self, program_data):
        """Установка/удаление программы"""
        current_state = config.is_program_installed(program_data["key"])
        new_state = not current_state

        if new_state:
            # Устанавливаем программу
            if self.installProgram(program_data):
                config.set_program_installed(program_data["key"], True, "1.0.0")
                QMessageBox.information(self, "Успех",
                                      f"Программа {program_data['name']} установлена!")
            else:
                QMessageBox.warning(self, "Ошибка",
                                  f"Не удалось установить {program_data['name']}")
        else:
            # Удаляем программу
            if self.uninstallProgram(program_data):
                config.set_program_installed(program_data["key"], False)
                QMessageBox.information(self, "Успех",
                                      f"Программа {program_data['name']} удалена!")
            else:
                QMessageBox.warning(self, "Ошибка",
                                  f"Не удалось удалить {program_data['name']}")

        # Обновляем интерфейс
        self.initUI()

    def installProgram(self, program_data):
        """Установка программы (заглушка)"""
        # TODO: Реализовать фактическую установку программы
        print(f"Установка {program_data['name']}")
        return True

    def uninstallProgram(self, program_data):
        """Удаление программы (заглушка)"""
        # TODO: Реализовать фактическое удаление программы
        print(f"Удаление {program_data['name']}")
        return True
