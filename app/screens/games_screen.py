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


class GamesScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Основной layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Заголовок
        title_label = QLabel("Исправления для игр")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white; margin: 10px;")

        main_layout.addWidget(title_label)

        # Описание
        desc_label = QLabel("Выберите исправление для конкретной игры:")
        desc_label.setStyleSheet("color: #cccccc; font-size: 14px; margin: 10px;")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(desc_label)

        # Создание scroll area
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.setSpacing(15)

        # Кнопки исправлений для игр
        games_fixes = [
            {
                "name": "Исправление The Crew",
                "key": "the_crew",
                "description": "Исправление проблем с запуском и работой The Crew"
            },
            {
                "name": "Исправление Forza Horizon",
                "key": "forza_horizon",
                "description": "Оптимизация производительности Forza Horizon"
            },
            {
                "name": "Исправление Hogwarts Legacy",
                "key": "hogwarts_legacy",
                "description": "Исправление лагов и вылетов Hogwarts Legacy"
            }
        ]

        for game in games_fixes:
            game_widget = self.createGameWidget(game)
            scroll_layout.addWidget(game_widget)

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

    def createGameWidget(self, game_data):
        """Создание виджета для исправления игры"""
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

        name_label = QLabel(game_data["name"])
        name_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")

        desc_label = QLabel(game_data["description"])
        desc_label.setStyleSheet("color: #cccccc; font-size: 12px;")
        desc_label.setWordWrap(True)

        text_layout.addWidget(name_label)
        text_layout.addWidget(desc_label)
        text_layout.addStretch(1)

        # Кнопка применения
        fix_button = QPushButton("Применить")
        fix_button.setMinimumWidth(120)
        fix_button.setMinimumHeight(40)

        # Проверяем статус исправления
        is_fixed = config.is_game_fixed(game_data["key"])
        if is_fixed:
            fix_button.setText("Убрать")
            fix_button.setStyleSheet("""
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
        else:
            fix_button.setText("Применить")
            fix_button.setStyleSheet("""
                QPushButton {
                    background-color: #5d4e7b;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #6d5d8a;
                }
            """)

        # Подключаем обработчик
        fix_button.clicked.connect(lambda checked, g=game_data: self.toggleGameFix(g))

        layout.addLayout(text_layout)
        layout.addWidget(fix_button)

        widget.setLayout(layout)
        return widget

    def toggleGameFix(self, game_data):
        """Применение/снятие исправления для игры"""
        current_state = config.is_game_fixed(game_data["key"])
        new_state = not current_state

        if new_state:
            # Применяем исправление
            if self.applyGameFix(game_data):
                config.set_game_fixed(game_data["key"], True)
                QMessageBox.information(self, "Успех",
                                      f"Исправление для {game_data['name']} применено!")
            else:
                QMessageBox.warning(self, "Ошибка",
                                  f"Не удалось применить исправление для {game_data['name']}")
        else:
            # Убираем исправление
            if self.removeGameFix(game_data):
                config.set_game_fixed(game_data["key"], False)
                QMessageBox.information(self, "Успех",
                                      f"Исправление для {game_data['name']} убрано!")
            else:
                QMessageBox.warning(self, "Ошибка",
                                  f"Не удалось убрать исправление для {game_data['name']}")

        # Обновляем интерфейс
        self.initUI()

    def applyGameFix(self, game_data):
        """Применение исправления для игры (заглушка)"""
        # TODO: Реализовать фактическое применение исправления
        print(f"Применение исправления для {game_data['name']}")
        return True

    def removeGameFix(self, game_data):
        """Удаление исправления для игры (заглушка)"""
        # TODO: Реализовать фактическое удаление исправления
        print(f"Удаление исправления для {game_data['name']}")
        return True
